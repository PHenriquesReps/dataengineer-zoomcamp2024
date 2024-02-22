{{ config(materialized='view') }}

select
--identifiers
    --{{ dbt_utils.generate_surrogate_key(['dispatching_base_num', 'pickup_datetime']) }} as tripid,
    dispatching_base_num,
    Affiliated_base_number,
    CAST(PUlocationID AS integer) as pickup_locationid,
    CAST(DOlocationID AS integer) as dropoff_locationid,

-- timestamps
    CAST(pickup_datetime as timestamp) as pickup_datetime,
    CAST(dropOff_datetime as timestamp) as dropoff_datetime,

    SR_Flag

from {{ source('staging','fhv_taxi') }}

-- dbt build --select <model.sql> --vars '{'is_test_run': 'False'}'
{% if var('is_test_run', default=True) %}

    limit 100

{% endif %}