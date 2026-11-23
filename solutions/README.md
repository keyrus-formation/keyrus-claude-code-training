# Corrigés (réservés au formateur)

> **Retirer ce dossier** de la copie distribuée aux participants (garder une branche privée `formateur`),
> et l'ouvrir à tous en fin de formation.

| Fichier | Exercice |
| --- | --- |
| `CLAUDE.md` | 1.3 — `CLAUDE.md` du projet (à copier à la racine) |
| `dbt_project/models/marts/dim_customers.sql` | 2.2 — migration de la requête LTV |
| `src/retail_pipeline/monthly_report.py` | 2.3 — rapport optimisé (≈ 90 s → 0,2 s, résultat identique) |
| `src/retail_pipeline/transform.py`, `tests/test_regressions.py` | 3.1 — les 4 bugs et leurs tests (6 tests échouent sur le code d'origine) |
| `dbt_project/models/marts/fct_orders.sql`, `_marts.yml` | 3.1 — correction du fan-out |
| `src/retail_pipeline/quality.py`, `dbt_project/tests/assert_payments_reconcile_with_orders.sql` | 3.2 — contrôles de qualité |
| `dbt_project/models/marts/mart_customers_at_risk.sql` (+ YAML, test singulier) | 4.2 — cas pratique, modèle dbt |
| `src/retail_pipeline/export_at_risk.py`, `tests/test_export_at_risk.py` | 4.2 — cas pratique, export pseudonymisé |

## Appliquer tous les corrigés (vérification formateur)

```bash
cp solutions/src/retail_pipeline/*.py src/retail_pipeline/
cp solutions/tests/*.py tests/
cp solutions/dbt_project/models/marts/* dbt_project/models/marts/
cp solutions/dbt_project/tests/* dbt_project/tests/
pytest -q                                              # 15 tests verts
python -m retail_pipeline.pipeline
cd dbt_project && DBT_PROFILES_DIR=. dbt build         # 26 PASS, 0 erreur
```
