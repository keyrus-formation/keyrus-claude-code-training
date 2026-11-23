-- Vérifie la règle métier ligne à ligne et l'absence de délai négatif. Renvoie les lignes en erreur.
select *
from {{ ref('mart_customers_at_risk') }}
where days_since_last_order < 0
   or (is_at_risk and (orders_last_12m < 2 or days_since_last_order <= inactivity_threshold_days))
   or (not is_at_risk and orders_last_12m >= 2 and days_since_last_order > inactivity_threshold_days)
