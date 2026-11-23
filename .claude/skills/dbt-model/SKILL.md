---
name: dbt-model
description: Crée ou refactore un modèle dbt selon les conventions Keyrus (staging → marts, tests, documentation). Use when the user asks to create, migrate or refactor a dbt model or to convert a legacy SQL query into dbt.
argument-hint: "[nom_du_modele] [description du besoin]"
allowed-tools: Read Grep Glob Edit Write Bash(dbt parse *) Bash(dbt build *) Bash(dbt compile *)
---

# Créer un modèle dbt (conventions Keyrus)

Besoin : $ARGUMENTS

## Étapes

1. **Comprendre le grain.** Avant d'écrire du SQL, énonce en une phrase le grain du modèle
   (« une ligne par … ») et la clé primaire. Si le besoin est ambigu, pose la question.
2. **Réutiliser l'existant.** Cherche les modèles `stg_*` existants dans `dbt_project/models/staging/`
   et les macros dans `dbt_project/macros/` (ex. `parse_amount`). Ne relis jamais une source brute
   depuis un mart : passe toujours par `ref('stg_…')`.
3. **Écrire le modèle** dans le bon dossier :
   - `staging/stg_<source>.sql` : typage, renommage, dédoublonnage. Matérialisation `view`.
   - `marts/fct_<processus>.sql` ou `marts/dim_<entite>.sql` : logique métier. Matérialisation `table`.
   - Style : CTE nommées (`with source as (…), renamed as (…)`), `select *` final, mots-clés en minuscules,
     une colonne par ligne, pas de `select *` sur une source brute.
   - Portabilité : le SQL doit tourner sur DuckDB **et** Snowflake. Utilise les macros ou `{% if target.type == 'snowflake' %}`
     pour les fonctions qui diffèrent (`try_to_number` vs `try_cast`, `datediff`, etc.).
4. **Agréger avant de joindre.** Toute table « enfant » (paiements, lignes de commande) jointe à un modèle de grain
   supérieur est d'abord agrégée au grain cible, pour éviter le *fan-out*.
5. **Tester** dans le YAML du dossier (`_marts.yml` / `_staging.yml`) :
   - `unique` + `not_null` sur la clé primaire (obligatoire),
   - `relationships` vers les dimensions,
   - `accepted_values` sur les colonnes catégorielles,
   - un test singulier dans `dbt_project/tests/` pour chaque règle métier non triviale.
6. **Documenter** : `description` du modèle (avec le grain) et des colonnes calculées.
7. **Valider** : `cd dbt_project && DBT_PROFILES_DIR=. dbt build --select <modele>+` et corrige jusqu'à ce que tout passe.
8. **Rendre compte** : résume le grain, les tests ajoutés et le résultat de `dbt build`.
