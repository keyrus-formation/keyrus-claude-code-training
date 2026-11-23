# RetailCo — pipeline data (Python + dbt, DuckDB en dev / Snowflake en recette)

Projet fil rouge Keyrus. Données de ventes fictives d'un distributeur (clients, commandes, paiements).

## Commandes
- Installer : `pip install -e ".[dev]"`
- Tests Python : `pytest -q` — lint : `ruff check src tests`
- Recharger l'entrepôt local : `python scripts/generate_data.py && python -m retail_pipeline.pipeline`
- dbt : `cd dbt_project && DBT_PROFILES_DIR=. dbt build --select <modele>+` (cible DuckDB par défaut)
- Snowflake : ajouter `--target snowflake`, **uniquement après accord explicite**

## Architecture
- `src/retail_pipeline/` : extract (CSV brut, tout en texte) → transform → quality → load (DuckDB/Snowflake)
- `dbt_project/models/staging` (vues, typage + dédoublonnage) → `marts` (tables, logique métier)
- Les transformations « officielles » vivent dans dbt ; le Python sert à l'ingestion et aux contrôles.

## Pièges métier connus (IMPORTANT)
- Montants sources en deux formats : `1234.50` et français `1 234,50` (espace = séparateur de milliers).
- `orders` contient plusieurs versions d'une même commande (CDC) : garder la plus récente (`updated_at` max).
- Une commande peut avoir 2 paiements (carte + bon d'achat) : agréger `payments` par `order_id` avant toute jointure.
- `FX_TO_EUR[devise]` = valeur d'une unité de devise en EUR : montant_eur = montant × taux.
- Dates futures et montants négatifs existent dans la source : les signaler, ne pas les supprimer en silence.

## Conventions
- Toute correction de bug = un test de non-régression qui échoue avant le correctif.
- Modèles dbt : grain dans la description, `unique` + `not_null` sur la clé, SQL portable via `macros/`.
- Python : typage, docstrings en français, pas d'`iterrows`, `logging` plutôt que `print`.
- Commits : `type(scope): message` (feat, fix, refactor, test, docs), en français.

## Sécurité
- Ne jamais lire `.env` ni afficher d'identifiants. Ne jamais modifier `data/raw/`.
- N'afficher que des agrégats ou au plus 20 lignes de données clients.

## Compaction
Lors d'un /compact, conserver : fichiers modifiés, commandes de test et leur dernier résultat, décisions prises.
