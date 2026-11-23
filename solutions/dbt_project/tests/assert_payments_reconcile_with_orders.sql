-- Test singulier : la somme payée dans fct_orders doit égaler la somme des paiements bruts.
-- Détecte toute réintroduction d'un fan-out ou d'une perte de lignes. Renvoie une ligne si KO.
with fact as (
    select sum(paid_amount) as total from {{ ref('fct_orders') }}
),
src as (
    select sum(amount) as total from {{ ref('stg_payments') }}
)
select fact.total as fact_total, src.total as source_total
from fact, src
where abs(fact.total - src.total) > 0.01
