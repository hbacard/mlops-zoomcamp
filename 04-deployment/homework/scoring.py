import argparse

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

import pickle
import pandas as pd


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

# %%
df.head()

# %%
dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)


# %%
print(f"Standard deviation predicted duration: {y_pred.std()}")
print(f"Mean predicted duration: {y_pred.mean()}")




# %%
df_result = pd.concat([df.ride_id, pd.DataFrame(y_pred, columns=["predictions"])], axis=1)
df_result.head()

# %%
# output_file = f"output_file_{year:04d}-{month:02d}.parquet"
# df_result.to_parquet(
#     output_file,
#     engine='pyarrow',
#     compression=None,
#     index=False
# )

# %%
# ! du -h output_file.parquet

# %% [markdown]
# ### Answer to Q2: 66M

# %% [markdown]
# 


