---
paths:
  - "src/**/*.py"
  - "tests/**/*.py"
---

# Règles Python

- Python 3.10+, annotations de type sur toutes les fonctions publiques, docstring en français.
- pandas : pas de `iterrows()` ni de `apply(axis=1)` sur plus de quelques milliers de lignes ; vectoriser ou passer par DuckDB.
- Chaque correction de bug s'accompagne d'un test de non-régression dans `tests/` qui échoue avant le correctif.
- Pas de `print` dans `src/` : utiliser `logging`.
