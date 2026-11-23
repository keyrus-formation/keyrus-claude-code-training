# J3 — Fiabiliser et outiller

Créez une branche `fix/<votre-nom>` avant de commencer.

---

## Exercice 3.1 — La chasse aux bugs (55 min)

> Message du contrôle de gestion : « Le chiffre d'affaires de la table `fct_orders` est plus élevé que celui de la comptabilité,
> et pourtant certaines grosses commandes B2B n'apparaissent avec aucun montant. Les montants en dollars semblent bizarres aussi.
> Et le taux de retour est bien plus bas que ce que voit le service client. »

Le pipeline Python (`src/retail_pipeline/transform.py`) et le modèle dbt `fct_orders` contiennent **plusieurs bugs**.
Les tests unitaires existants passent tous.

Pour **chaque** bug trouvé :
1. écrivez (faites écrire) un test qui **échoue** sur le code actuel — montrez l'échec ;
2. trouvez la cause racine et corrigez-la, sans changement hors sujet ;
3. vérifiez : `pytest -q` et `dbt build` ;
4. chiffrez l'impact sur les données (lignes et euros concernés) ;
5. commitez séparément : `fix(scope): description`.

Règles : interdit de modifier un test existant pour le faire passer, interdit d'ajouter un `DISTINCT` pour masquer un doublon, interdit d'avaler une exception.

Tenez à jour ce tableau :

| # | Fichier / fonction | Cause | Test ajouté | Impact |
| --- | --- | --- | --- | --- |
| | | | | |

---

## Exercice 3.2 — Contrôles de qualité (25 min)

1. Lancez `/data-quality-audit data/raw/orders.csv`. Comparez avec ce que vous savez déjà.
2. Complétez les 4 fonctions marquées `TODO` dans [`src/retail_pipeline/quality.py`](../src/retail_pipeline/quality.py), avec leurs tests unitaires.
3. Côté dbt, ajoutez :
   - `relationships` de `fct_orders.customer_id` vers `stg_customers` ;
   - un **test singulier** `dbt_project/tests/assert_payments_reconcile_with_orders.sql` qui vérifie que la somme payée dans `fct_orders` égale la somme des paiements bruts.
4. Les anomalies de la source (montants négatifs, dates futures, emails vides) doivent être **signalées**, pas supprimées. Où et comment les signalez-vous ?

---

## Exercice 3.3 — Brancher le serveur MCP dbt (15 min)

Prérequis : `uv` installé.

```bash
claude mcp add dbt \
  -e DBT_PROJECT_DIR="$PWD/dbt_project" -e DBT_PATH="$(which dbt)" -e DBT_PROFILES_DIR="$PWD/dbt_project" \
  -- uvx dbt-mcp
```

1. Dans Claude Code, `/mcp` : le serveur est-il connecté ? Quels outils propose-t-il ?
2. Avec le serveur MCP, produisez la matrice : modèle → tests → colonnes **non** testées.
3. Comparez avec la même demande faite sans MCP (`/mcp` pour le désactiver) : résultat, nombre d'actions, consommation (`/usage`).

---

## Exercice 3.4 — Votre propre automatisation (15 min)

Au choix :

**A. Un skill** `/explain-model <modele>` dans `.claude/skills/explain-model/SKILL.md` qui documente un modèle dbt : grain, lignage amont/aval, tests, colonnes non testées, et propose les tests manquants. Testez-le sur `fct_orders` et `stg_orders`.

**B. Un hook** `Stop` dans `.claude/settings.json` qui lance `pytest -q` à la fin de chaque réponse de Claude et, en cas d'échec, lui renvoie les tests en erreur (code de sortie 2). Attention aux boucles infinies : que se passe-t-il si les tests restent rouges ? (Le JSON reçu par le hook contient `stop_hook_active`.)

**C. Un script non interactif** `scripts/nightly_quality.sh` qui appelle `claude -p` en mode `dontAsk` avec une liste blanche d'outils pour produire `reports/qualite.md`.
