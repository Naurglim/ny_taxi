# BigQuery Homework


## Retrieving the data and loading it to Google Cloud Storage (GCS)

To prepare the stage for this week's homework we first need to gather our data. 
In this case, it will be the <b>2022 green taxi data</b> from the [New York City Taxi Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

I made a script to download the specific files we need to the local storage and then upload them to GCS
```bash
python3 data_import.py {--service SERVICE} {--year YEAR} {--year YEAR} ... {--year YEAR}
```

It takes the taxi service [yellow, green, fhv, fhvhv] as it's first parameter and then any number of years as optional parameters.
It will gather all monthly files for the specified years. 
For it to work you'll need to set up the following environment variables:
 - `GCP_GCS_BUCKET` with the name of your destination GCS bucket. 
 - `GCP_GCS_CREDENTIALS` with the location of you .json credentials.

For this excercise we will run this script with the following parameters: 
```bash
python3 data_import.py green 2022
```


## Building our BigQuery Data Warehouse from the files in the GCS Bucket

From there, we can create the tables we need in a BigQuery dataset (I used the dataset I created in the first week):


### Create external table:
```sql
CREATE OR REPLACE EXTERNAL TABLE ny_taxi_week3.external_green_tripdata_2022
OPTIONS (
  format = 'parquet',
  uris = ['https://storage.cloud.google.com/ny-rides-gperezcenteno-411315-terra-bucket/green/green_tripdata_2022-*.parquet']
); 
```

### Create materialized table from external:
```sql
CREATE OR REPLACE TABLE ny_taxi_week3.green_tripdata_2022_non_partitioned AS
SELECT * FROM ny_taxi_week3.external_green_tripdata_2022;
```

### Create partitioned table from external:
```sql
CREATE OR REPLACE TABLE ny_taxi_week3.green_tripdata_2022_partitioned
PARTITION BY DATE(lpep_pickup_datetime) 
CLUSTER BY PULocationID 
AS (
  SELECT * FROM ny_taxi_week3.external_green_tripdata_2022
);
```

And then, we can run the queries we need to get the answers to the homework questions from the tables we created:

### Question 2:
```sql
SELECT count(DISTINCT PULocationID) FROM ny_taxi_week3.external_green_tripdata_2022;
-- 0.00 MB
```
```sql
SELECT count(DISTINCT PULocationID) FROM ny_taxi_week3.green_tripdata_2022_non_partitioned;
-- 6.41 MB
```

### Question 3:
```sql
SELECT count(*) FROM ny_taxi_week3.green_tripdata_2022_non_partitioned WHERE fare_amount = 0;
-- 1622
```

### Question 5:
```sql
SELECT DISTINCT PULocationID 
FROM ny_taxi_week3.green_tripdata_2022_non_partitioned 
WHERE lpep_pickup_datetime between '2022-06-01' AND '2022-06-30';
-- 12.82 MB
```
```sql
SELECT DISTINCT PULocationID 
FROM ny_taxi_week3.green_tripdata_2022_partitioned 
WHERE lpep_pickup_datetime between '2022-06-01' AND '2022-06-30';
-- 1.12 MB
```