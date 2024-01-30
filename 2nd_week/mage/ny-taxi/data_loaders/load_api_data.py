import io
import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):

    base_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/'
    files_to_retrieve = ['green_tripdata_2020-10.csv.gz', 
                         'green_tripdata_2020-11.csv.gz', 
                         'green_tripdata_2020-12.csv.gz']
    taxi_dtypes = {
                    'VendorID': pd.Int64Dtype(),
                    'passenger_count': pd.Int64Dtype(),
                    'trip_distance': float,
                    'RatecodeID':pd.Int64Dtype(),
                    'store_and_fwd_flag':str,
                    'PULocationID':pd.Int64Dtype(),
                    'DOLocationID':pd.Int64Dtype(),
                    'payment_type': pd.Int64Dtype(),
                    'trip_type': pd.Int64Dtype(),
                    'fare_amount': float,
                    'extra':float,
                    'mta_tax':float,
                    'tip_amount':float,
                    'tolls_amount':float,
                    'improvement_surcharge':float,
                    'total_amount':float,
                    'congestion_surcharge':float
                }
    # Date parsing 
    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
    
    dfs = []
    for filename in files_to_retrieve:
        url = base_url + filename
        df = pd.read_csv(url, sep=',', compression='gzip', dtype = taxi_dtypes, parse_dates=parse_dates, header=0)
        df['source_file'] = filename
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
