-- Une ligne par commande : on garde la version la plus récente (updated_at max).
with source as (
    select * from {{ source('raw', 'orders') }}
),

typed as (
    select
        order_id,
        customer_id,
        cast(order_ts as timestamp)    as order_ts,
        channel,
        status,
        currency,
        {{ parse_amount('total_amount') }} as total_amount,
        cast(updated_at as timestamp)  as updated_at
    from source
),

deduplicated as (
    select *
    from typed
    qualify row_number() over (partition by order_id order by updated_at desc) = 1
)

select * from deduplicated
