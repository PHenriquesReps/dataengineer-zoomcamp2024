{{ config(materialized='view') }}

with tripdata as 
(
  select *,
    row_number() over(partition by vendorid, tpep_pickup_datetime) as rn
  from {{ source('staging','yellow_taxi') }}
  where vendorid is not null 
)
select
--identifiers
    {{ dbt_utils.generate_surrogate_key(['vendorid', 'tpep_pickup_datetime']) }} as tripid,
    CAST(VendorID AS integer) as vendorid,
    CAST(RatecodeID AS integer) as ratecodeid,
    CAST(PULocationID AS integer) as pickup_locationid,
    CAST(DOLocationID AS integer) as dropoff_locationid,

-- timestamps
    CAST(tpep_pickup_datetime as timestamp) as pickup_datetime,
    CAST(tpep_dropoff_datetime as timestamp) as dropoff_datetime,

--trip info
    store_and_fwd_flag,
    CAST(passenger_count AS integer) as passenger_count,
    CAST(trip_distance AS numeric) as trip_distance,
    -- yellow cabs are always street-hail
    1 as trip_type,

-- payment info
    CAST(fare_amount AS numeric) as fare_amount,
    CAST(extra AS numeric) as extra,
    CAST(mta_tax AS numeric) as mta_tax,
    CAST(tip_amount AS numeric) as tip_amount,
    CAST(tolls_amount AS numeric) as tolls_amount,
    0 as ehail_fee,
    CAST(improvement_surcharge AS numeric) as improvement_surcharge,
    CAST(total_amount AS numeric) as total_amount,
    CAST(payment_type as integer) as payment_type,
    {{ get_payment_type_description('payment_type') }} as payment_type_description,
    CAST(congestion_surcharge AS numeric) as congestion_surcharg

from tripdata
where rn = 1

-- dbt build --select <model.sql> --vars '{'is_test_run': 'False'}'
{% if var('is_test_run', default=True) %}

    limit 100

{% endif %}