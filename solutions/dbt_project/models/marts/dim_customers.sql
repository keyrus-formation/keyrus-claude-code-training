-- Dimension clients enrichie de la valeur vie client (migration de sql/legacy/customer_ltv.sql).
-- Grain : une ligne par client (customer_id).
-- Écarts assumés vs la requête historique (validés avec le métier) :
--   * nb_orders exclut désormais les commandes annulées (cohérent avec total_revenue) ;
--   * total_paid n'est plus gonflé par les versions multiples de commandes (stg_orders dédoublonné) ;
--   * les montants au format '1 234,50' ne sont plus perdus (macro parse_amount).
with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('fct_orders') }}
    where status <> 'cancelled'
),

customer_orders as (
    select
        customer_id,
        count(*)            as nb_orders,
        sum(total_amount)   as total_revenue,
        sum(paid_amount)    as total_paid,
        max(order_ts)       as last_order_ts
    from orders
    group by customer_id
)

select
    c.customer_id,
    upper(c.first_name) || ' ' || upper(c.last_name)  as customer_name,
    c.segment,
    c.city,
    coalesce(o.nb_orders, 0)                           as nb_orders,
    coalesce(o.total_revenue, 0)                       as total_revenue,
    coalesce(o.total_paid, 0)                          as total_paid,
    o.last_order_ts,
    {{ dbt.datediff('o.last_order_ts', 'current_date', 'day') }} as days_since_last_order
from customers c
left join customer_orders o on o.customer_id = c.customer_id
