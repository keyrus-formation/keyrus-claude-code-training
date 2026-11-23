with source as (
    select distinct * from {{ source('raw', 'customers') }}
)

select
    customer_id,
    first_name,
    last_name,
    nullif(lower(trim(email)), '') as email,
    nullif(city, '')               as city,
    segment,
    cast(signup_date as date)      as signup_date
from source
