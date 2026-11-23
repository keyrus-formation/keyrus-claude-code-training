-- Table de faits commandes : une ligne par commande (grain = order_id).
-- NOTE FORMATEUR : contient un bug de jointure volontaire (exercice J3).
with orders as (
    select * from {{ ref('stg_orders') }}
),

payments as (
    select * from {{ ref('stg_payments') }}
)

select
    o.order_id,
    o.customer_id,
    o.order_ts,
    o.channel,
    o.status,
    o.currency,
    o.total_amount,
    p.amount                         as paid_amount,
    p.amount >= o.total_amount       as is_fully_paid
from orders o
left join payments p on p.order_id = o.order_id
