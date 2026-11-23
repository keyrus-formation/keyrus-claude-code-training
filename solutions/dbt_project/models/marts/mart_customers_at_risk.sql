-- Clients à risque de départ (cas pratique J4).
-- Grain : une ligne par client (customer_id), tous les clients.
-- Règle métier : aucune commande non annulée depuis > 90 jours (> 60 pour les VIP)
-- ET au moins 2 commandes non annulées dans les 365 jours précédant as_of_date.
{% set as_of_date = var('as_of_date', '2026-09-01') %}

with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select
        customer_id,
        order_id,
        cast(order_ts as date) as order_date,
        total_amount
    from {{ ref('fct_orders') }}
    where status in ('delivered', 'shipped', 'returned')
      and cast(order_ts as date) <= cast('{{ as_of_date }}' as date)   -- ignore les dates futures
),

per_customer as (
    select
        customer_id,
        max(order_date) as last_order_date,
        count(case when order_date > cast('{{ as_of_date }}' as date) - interval '365 days'
                   then order_id end)                              as orders_last_12m,
        sum(case when order_date > cast('{{ as_of_date }}' as date) - interval '365 days'
                 then total_amount else 0 end)                     as revenue_last_12m
    from orders
    group by customer_id
),

scored as (
    select
        c.customer_id,
        c.email,
        c.segment,
        p.last_order_date,
        {{ dbt.datediff('p.last_order_date', "cast('" ~ as_of_date ~ "' as date)", 'day') }} as days_since_last_order,
        coalesce(p.orders_last_12m, 0)   as orders_last_12m,
        coalesce(p.revenue_last_12m, 0)  as revenue_last_12m,
        case when c.segment = 'VIP' then 60 else 90 end as inactivity_threshold_days
    from customers c
    left join per_customer p on p.customer_id = c.customer_id
)

select
    *,
    coalesce(days_since_last_order > inactivity_threshold_days and orders_last_12m >= 2, false)
        as is_at_risk,
    cast('{{ as_of_date }}' as date) as as_of_date
from scored
