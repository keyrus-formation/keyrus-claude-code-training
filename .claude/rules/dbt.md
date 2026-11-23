---
paths:
  - "dbt_project/**/*.sql"
  - "dbt_project/**/*.yml"
---

# Règles dbt (chargées uniquement quand Claude travaille sur des fichiers dbt)

- Toujours `ref()` / `source()`, jamais de nom de table en dur.
- Toute nouvelle table de faits déclare son grain dans sa `description` et a un test `unique` + `not_null` sur sa clé.
- Agréger les tables enfants (paiements, lignes) avant de les joindre à un grain supérieur.
- SQL portable DuckDB / Snowflake : passer par les macros de `dbt_project/macros/`.
- Commande de validation : `cd dbt_project && DBT_PROFILES_DIR=. dbt build --select <modele>+`.
