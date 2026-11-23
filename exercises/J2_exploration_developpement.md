# J2 — Comprendre un existant et produire du code Data

Partez de votre branche de J1 (ou de la branche `etat-J2`). Pensez à `/clear` entre deux exercices.

---

## Exercice 2.1 — Cartographier RetailCo (35 min)

Objectif : produire `docs/ARCHITECTURE.md`, compréhensible en 5 minutes par un nouvel arrivant.

Contenu attendu :
1. un schéma **Mermaid** du flux : CSV bruts → pipeline Python → DuckDB/Snowflake → modèles staging → marts ;
2. un tableau des modèles dbt : nom, grain, matérialisation, tests ;
3. les dépendances Python déclarées vs réellement importées ;
4. le lignage de `fct_orders` (utilisez `dbt ls --select +fct_orders`) ;
5. une section **« Zones de risque »** (au moins 3, avec fichier et ligne) et une section **« Questions ouvertes pour le métier »**.

Contrainte : restez en Plan Mode ou en mode `default` pendant l'exploration ; ne laissez écrire que le fichier `docs/ARCHITECTURE.md`.
Vérification : cochez dans le document chaque affirmation que **vous** avez vérifiée vous-même. Combien en avez-vous trouvé d'inexactes ?

🚀 Pour aller plus loin : demandez à Claude d'utiliser des subagents en parallèle (un pour `src/`, un pour `dbt_project/`) et comparez la consommation (`/usage`).

---

## Exercice 2.2 — Migrer une requête Snowflake en modèle dbt (50 min, binômes)

La requête [`sql/legacy/customer_ltv.sql`](../sql/legacy/customer_ltv.sql) tourne chaque nuit sur Snowflake. Elle doit devenir le modèle `dbt_project/models/marts/dim_customers.sql`.

1. **Explorer (Plan Mode)** : faites lister par Claude tous les problèmes de la requête (performance, exactitude, portabilité). Complétez avec ce que vous aviez noté vous-mêmes.
2. **Planifier** : grain, modèles réutilisés, colonnes, tests. Validez le plan en binôme.
3. **Implémenter** : SQL portable DuckDB/Snowflake (macros du projet), YAML avec description et tests.
4. **Vérifier** : `cd dbt_project && DBT_PROFILES_DIR=. dbt build --select +dim_customers`.
5. **Comparer** : pour 5 clients, comparez vos chiffres avec ceux de l'ancienne logique (exécutée sur DuckDB). **Expliquez chaque écart** dans la description du modèle.

Question à se poser à la fin : votre `dbt build` complet est-il entièrement vert ?

🚀 Pour aller plus loin : rendez `fct_orders` incrémental (`materialized='incremental'`, `unique_key='order_id'`, stratégie `merge` sur Snowflake), filtré sur `updated_at`.

---

## Exercice 2.3 — Optimiser le rapport historique (35 min)

[`src/retail_pipeline/legacy_report.py`](../src/retail_pipeline/legacy_report.py) calcule le chiffre d'affaires mensuel par catégorie. Il met environ 90 secondes.

Objectif : nouveau module `src/retail_pipeline/monthly_report.py`, moins d'une seconde, **résultat strictement identique**.

Méthode imposée (à donner à Claude) :
1. exécuter **une seule fois** l'ancien rapport et sauvegarder sa sortie comme référence (`tests/fixtures/monthly_report_reference.csv`) ;
2. diagnostiquer les causes de lenteur ;
3. réécrire (pandas vectorisé ou DuckDB), avec typage et docstrings ;
4. écrire un test qui compare la nouvelle sortie à la référence ;
5. mesurer le gain.

Question de fond : l'ancien rapport fait-il un choix métier discutable sur les commandes présentes plusieurs fois ? Faut-il le reproduire ou le corriger ? Qui décide ?
