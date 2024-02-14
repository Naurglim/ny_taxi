import requests
import os
import sys
from google.cloud import storage


TRIP_CLASSES = ['fhv','fhvhv','green','yellow']
AVAILABLE_YEARS = [str(x) for x in range(2009,2024)]
BASE_URL = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
FOLDER = 'data/'
BUCKET = os.environ.get("GCP_GCS_BUCKET", "ny-rides-gperezcenteno-411315-terra-bucket")  # Set up the env variable or change the default.
CREDENTIALS = os.environ.get("GCP_GCS_CREDENTIALS", "ny-rides.json")  # Set up the env variable or change the default.

def upload_to_gcs(bucket, object_name, local_file):
    client = storage.Client.from_service_account_json(CREDENTIALS)
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def download_file(trip_class, year, month):
    year_month = year + '-' + month
    file_name = f"{trip_class}_tripdata_{year_month}.parquet"
    request_url = f"{BASE_URL}{file_name}"
    local_path = f"{FOLDER}{file_name}"

    r = requests.get(request_url)
    with open(local_path, 'wb') as file:
        file.write(r.content)

    return file_name


def process_files(trip_class, years):
    for year in years:
        for i in range(12):
            month = ('0' + str(i+1))[-2:]
            file_name = download_file(trip_class, year, month)
            upload_to_gcs(BUCKET, f"{trip_class}/{file_name}", f"{FOLDER}{file_name}")


if __name__ == '__main__':
    if len(sys.argv) > 2:
        if sys.argv[1] in TRIP_CLASSES:
            trip_class = sys.argv[1]
            years = [sys.argv[i] for i in range(2,len(sys.argv)) if sys.argv[i] in AVAILABLE_YEARS]
            process_files(trip_class, years)

