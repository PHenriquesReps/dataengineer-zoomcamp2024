-- External Table Creation
CREATE OR REPLACE EXTERNAL TABLE `dataenginner-zoomcamp.taxi_data.external_green_tripdata_2022`
OPTIONS (
  format = 'parquet',
  uris = [
    'gs://ph-taxi-data/green_taxi/7d18ddad719a47b4b24a75a51e574046-0.parquet'
    ]
);


-- Internal Table Creation (Materialized Table)
CREATE OR REPLACE TABLE `dataenginner-zoomcamp.taxi_data.managed_green_tripdata` AS 
    Select 
        * 
    from 
        `taxi_data.external_green_tripdata_2022`;


-- Q1
SELECT COUNT(VendorID)
FROM `taxi_data.external_green_tripdata_2022`;


-- Q2

-- External
select count(distinct(PULocationID)) as dist_locations
from `taxi_data.external_green_tripdata_2022`;

-- Managed
select count(distinct(PULocationID)) as dist_locations
from `taxi_data.managed_green_tripdata`;


--Q3

select  fare_amount, count(*)
from `taxi_data.external_green_tripdata_2022`
where  fare_amount = 0
group by 1;


-- Create a Partitioned and Clustered Table
CREATE OR REPLACE TABLE `dataenginner-zoomcamp.taxi_data.green_tripdata_2022_partitioned_clustered`
PARTITION BY DATE(lpep_pickup_datetime )
CLUSTER BY PUlocationID AS 
    (
        SELECT 
            * 
        FROM 
            `dataenginner-zoomcamp.taxi_data.managed_green_tripdata`
    );


-- Q5

select 
    distinct(PULocationID)
from 
    `taxi_data.managed_green_tripdata`
where 
    cast(lpep_pickup_datetime as date) between '2022-06-01' and '2022-06-30';


select 
    distinct(PULocationID)
from 
    `dataenginner-zoomcamp.taxi_data.green_tripdata_2022_partitioned_clustered`
where 
    cast(lpep_pickup_datetime as date) between '2022-06-01' and '2022-06-30';
