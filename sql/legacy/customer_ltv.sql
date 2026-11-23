-- Valeur vie client (LTV) — requête historique Snowflake, exécutée chaque nuit.
-- Problèmes connus : lente (sous-requêtes corrélées), double comptage suspecté,
-- personne ne sait pourquoi le filtre sur 'VIP' est là.
-- Support des exercices J2 (refactoring en modèle dbt) et J3 (debugging).

SELECT
    c.customer_id,
    UPPER(c.first_name) || ' ' || UPPER(c.last_name) AS customer_name,
    c.segment,
    (SELECT COUNT(*) FROM raw.orders o WHERE o.customer_id = c.customer_id) AS nb_orders,
    (SELECT SUM(TRY_TO_NUMBER(REPLACE(o.total_amount, ',', '.'), 12, 2))
       FROM raw.orders o
      WHERE o.customer_id = c.customer_id
        AND o.status <> 'cancelled') AS total_revenue,
    (SELECT SUM(p.amount)
       FROM raw.orders o
       JOIN raw.payments p ON p.order_id = o.order_id
      WHERE o.customer_id = c.customer_id) AS total_paid,
    (SELECT MAX(o.order_ts) FROM raw.orders o WHERE o.customer_id = c.customer_id) AS last_order_ts,
    DATEDIFF('day', (SELECT MAX(o.order_ts) FROM raw.orders o WHERE o.customer_id = c.customer_id),
             CURRENT_DATE()) AS days_since_last_order
FROM raw.customers c
WHERE c.segment IN ('B2C', 'B2B', 'VIP')
ORDER BY total_revenue DESC NULLS LAST;
