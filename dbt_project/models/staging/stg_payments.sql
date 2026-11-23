select
    payment_id,
    order_id,
    method,
    cast(amount as decimal(12, 2)) as amount,
    cast(paid_at as timestamp)     as paid_at
from {{ source('raw', 'payments') }}
