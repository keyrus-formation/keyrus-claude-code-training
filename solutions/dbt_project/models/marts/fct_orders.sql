-- Table de faits commandes. Grain : une ligne par commande (order_id).
with orders as (
    select * from {{ ref('stg_orders') }}
),

-- Agrégation au grain commande AVANT jointure : une commande peut avoir 2 paiements
payments_per_order as (
    select
        order_id,
        sum(amount)  as paid_amount,
        count(*)     as nb_payments
    from {{ ref('stg_payments') }}
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    o.order_ts,
    o.channel,
    o.status,
    o.currency,
    o.total_amount,
    coalesce(p.paid_amount, 0)                as paid_amount,
    coalesce(p.nb_payments, 0)                as nb_payments,
    coalesce(p.paid_amount, 0) >= o.total_amount as is_fully_paid
from orders o
left join payments_per_order p on p.order_id = o.order_id
