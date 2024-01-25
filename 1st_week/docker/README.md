### Docker Homework

## Set up environment

First set up Postgres and PGAdmin:

```bash
docker-compose up -d
``` 
Data will persist on ´data/ny_taxi_postgres_data/´ and ´data/pgadmin_data/´ folder respectively (Make sure to set the right permissions on those folders)


## Ingestion

Build the image:

```bash
docker build -t taxi_ingest:v001 .
```

Then run the docker pipeline for each file you need to ingest:

* Green taxi data
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

docker run -it \
  --network=docker_default \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_taxi_trips \
    --url=${URL}
```

* Taxi Zones
```bash
URL="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

docker run -it \
  --network=docker_default \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=zones \
    --url=${URL}
```

## Data needed for Homework:

Original files
* [URL for Green taxi data] (https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz)
* [URL for Zones] (https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv)
