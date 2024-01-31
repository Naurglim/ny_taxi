import pyarrow as pa
from pyarrow import parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/ny-rides-gperezcenteno-411315-ad4a0f2cdf9a.json"

bucket_name = 'ny-rides-gperezcenteno-411315-terra-bucket'
project_id = 'ny-rides-gperezcenteno-411315'
table_name = 'nyc_taxi_data'

root_path = f"{bucket_name}/{table_name}"

@data_exporter
def export_data(data, *args, **kwargs):
    # Specify your data exporting logic here
    data['lpep_pickup_date']
    table = pa.Table.from_pandas(data)
    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path = root_path,
        partition_cols = ['lpep_pickup_date'],
        filesystem = gcs
    )


