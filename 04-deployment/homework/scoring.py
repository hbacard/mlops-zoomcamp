import argparse
import os
import boto3
import pickle
import pandas as pd
# Create the parser
parser = argparse.ArgumentParser(description='Process year and month.')

# Add the parameters
parser.add_argument('--year', type=int, required=True, help='The year to process')
parser.add_argument('--month', type=int, required=True, help='The month to process')

# Parse the arguments
args = parser.parse_args()

# Access the parameters
year = args.year
month = args.month

# getting env variables
BUCKET_NAME = os.environ.get("BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename, year=2023, month=3):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

# %%

df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet', year=year, month=month)


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)

print(f"Standard deviation predicted duration: {y_pred.std()}")
print(f"Mean predicted duration: {y_pred.mean()}")


df_result = pd.concat([df.ride_id, pd.DataFrame(y_pred, columns=["predictions"])], axis=1)

output_file = f"output_file_{year:04d}-{month:02d}.parquet"
df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)

s3 = boto3.client("s3",
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_DEFAULT_REGION)

def upload_to_s3(output_file, bucket_name: str = BUCKET_NAME, folder: str = None):
    file_name = output_file
    file_path = os.path.join(".", file_name)
    object_key = os.path.join(folder, file_name) if folder is not None else file_name

    try:
        # Upload the file
        response = s3.upload_file(file_path, bucket_name, object_key)
        print(f"{output_file} uploaded successfully.")
    except Exception as e:
        print("An error occurred:", e)

  
upload_to_s3(output_file=output_file, folder="parquets")
 


