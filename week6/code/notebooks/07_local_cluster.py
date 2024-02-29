#!/usr/bin/env python
# coding: utf-8

import argparse
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F



# This makes our code more configurable, we say from where it should read and write to, from the command line interface

parser = argparse.ArgumentParser(description='Ingest data to GCS')    # print in help
parser.add_argument('--input_green', help='green input file path')
parser.add_argument('--input_yellow', help='yellow input file path')
parser.add_argument('--output', help='output path')


args = parser.parse_args()


input_green = args.input_green          # '/home/pedroh/dataengineer-zoomcamp2024/week6/code/data/pq/green/*/*'
input_yellow = args.input_yellow        # '/home/pedroh/dataengineer-zoomcamp2024/week6/code/data/pq/yellow/*/*'
output = args.output                    # '/home/pedroh/dataengineer-zoomcamp2024/week6/code/data/report/revenue/'



spark = SparkSession.builder \
    .master("spark://de-zoomcamp.europe-west1-b.c.dataenginner-zoomcamp.internal:7077") \
    .appName('test') \
    .getOrCreate()



df_green = spark.read.parquet(input_green)


df_green = df_green \
    .withColumnRenamed('lpep_pickup_datetime', 'pickup_datetime') \
    .withColumnRenamed('lpep_dropoff_datetime', 'dropoff_datetime')

df_yellow = spark.read.parquet(input_yellow)



df_yellow = df_yellow \
    .withColumnRenamed('tpep_pickup_datetime', 'pickup_datetime') \
    .withColumnRenamed('tpep_dropoff_datetime', 'dropoff_datetime')



common_columns = ['VendorID',
 'pickup_datetime',
 'dropoff_datetime',
 'store_and_fwd_flag',
 'RatecodeID',
 'PULocationID',
 'DOLocationID',
 'passenger_count',
 'trip_distance',
 'fare_amount',
 'extra',
 'mta_tax',
 'tip_amount',
 'tolls_amount',
 'improvement_surcharge',
 'total_amount',
 'payment_type',
 'congestion_surcharge']



df_green_final = df_green.select(common_columns).withColumn('service_type', F.lit('Green'))


df_yellow_final = df_yellow.select(common_columns).withColumn('service_type', F.lit('Yellow'))


df_trips_data = df_green_final.unionAll(df_yellow_final)


df_trips_data.groupBy('service_type').count().show()


df_trips_data.createOrReplaceTempView('trips_data')


df_result = spark.sql("""
SELECT 
    -- Reveneue grouping 
     PULocationID AS revenue_zone,
     date_trunc('month', pickup_datetime) AS revenue_month,
     service_type, 

    -- Revenue calculation 
     ROUND(SUM(fare_amount),2) AS revenue_monthly_fare,
     ROUND(SUM(extra),2) AS revenue_monthly_extra,
     ROUND(SUM(mta_tax),2) AS revenue_monthly_mta_tax,
     ROUND(SUM(tip_amount),2) AS revenue_monthly_tip_amount,
     ROUND(SUM(tolls_amount),2) AS revenue_monthly_tolls_amount,
     ROUND(SUM(improvement_surcharge),2) AS revenue_monthly_improvement_surcharge,
     ROUND(SUM(total_amount),2) AS revenue_monthly_total_amount,
     ROUND(SUM(congestion_surcharge),2) AS revenue_monthly_congestion_surcharge,

    -- Additional calculations
     ROUND(AVG(passenger_count),2) AS avg_montly_passenger_count,
     ROUND(AVG(trip_distance),2) AS avg_montly_trip_distance
FROM
    trips_data
GROUP BY
    1, 2, 3
""")

df_result.write.parquet(output, mode='overwrite')


"""
Command to run the script on the command line

python 07_local_cluster.py \
    --input_green='/home/pedroh/dataengineer-zoomcamp2024/week6/code/data/pq/green/2020/*' \
    --input_yellow='/home/pedroh/dataengineer-zoomcamp2024/week6/code/data/pq/yellow/2020/*' \
    --output= '/home/pedroh/dataengineer-zoomcamp2024/week6/code/data/report-2020'

"""

