from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path
import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/dataenginner-zoomcamp-c7acd473c81f.json"

bucket_name = 'mage-zoomcamp-ph'
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
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs
    )
