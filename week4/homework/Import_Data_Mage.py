# Data Loader

import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

df_green_taxi = []
load_date = ['_2022-01','_2022-02','_2022-03','_2022-04','_2022-05','_2022-06','_2022-07','_2022-08','_2022-09','_2022-10', '_2020-11', '_2020-12']
@data_loader
def load_data_from_api(*args, **kwargs):


    for f in load_date:
        url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata{f}.parquet'
    
        df = pd.read_parquet(url)
        df_green_taxi.append(df)
        combined_df = pd.concat(df_green_taxi, ignore_index=True)

    return combined_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'



# Data Exporter

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path
import pyarrow as pa
import pyarrow.parquet as pq
import os
import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/dataenginner-zoomcamp-c7acd473c81f.json"

bucket_name = 'ph-taxi-data'
project_id = 'dataenginner-zoomcamp'

table_name = "green_taxi"

root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:

    
    table = pa.Table.from_pandas(df)      # reading the dataframe into a pyarrow table

    gcs = pa.fs.GcsFileSystem()     # find the google cloud storage object, that will authorize using the env var automatically

    
    
    pq.write_to_dataset(
        table,
        root_path=root_path,
        filesystem=gcs,
        use_deprecated_int96_timestamps=True
    )
