import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

df_green_taxi = []
load_date = ['_2020-10', '_2020-11', '_2020-12']
@data_loader
def load_data_from_api(*args, **kwargs):


    for f in load_date:
        url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata{f}.csv.gz'
        taxi_dtypes = {
                'VendorID': pd.Int64Dtype(),
                'passenger_count': pd.Int64Dtype(),
                'trip_distance': float,
                'RatecodeID':pd.Int64Dtype(),
                'store_and_fwd_flag':str,
                'PULocationID':pd.Int64Dtype(),
                'DOLocationID':pd.Int64Dtype(),
                'payment_type': pd.Int64Dtype(),
                'fare_amount': float,
                'extra':float,
                'mta_tax':float,
                'tip_amount':float,
                'tolls_amount':float,
                'improvement_surcharge':float,
                'total_amount':float,
                'congestion_surcharge':float
            }
        parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
    
        df = pd.read_csv(url,compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates)

        df_green_taxi.append(df)
            # Concatenate all DataFrames in the list
        combined_df = pd.concat(df_green_taxi, ignore_index=True)

    return combined_df



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'