import requests
from io import BytesIO
from typing import List

import pandas as pd

# base_url_green_taxi = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata'
base_url_yellow_taxi = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata'

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def ingest_files(**kwargs) -> pd.DataFrame:
    dfs: List[pd.DataFrame] = []

    for year, months in [(2023, (3, 4))]:
        for i in range(*months):
            response = requests.get(
                base_url_yellow_taxi + f'_{year}-{i:02d}.parquet'
            )

            if response.status_code != 200:
                raise Exception(response.text)

            df = pd.read_parquet(BytesIO(response.content))
            dfs.append(df)

    return pd.concat(dfs)