# Après-midi 2 — Comprendre un existant et produire du code Data

**Thèmes couverts** : 3. Compréhension et exploration de code · 4. Développement Data assisté par IA
**Exercices participants** : [`exercises/J2_exploration_developpement.md`](../exercises/J2_exploration_developpement.md)

| Horaire | Durée | Séquence | Format |
| --- | --- | --- | --- |
| 13 h 30 | 10 min | Retour sur J1 : un `CLAUDE.md` montré à l'écran | Échange |
| 13 h 40 | 25 min | 3.1 Explorer un dépôt inconnu | Exposé + démo |
| 14 h 05 | 35 min | **Exercice 2.1** — Cartographier RetailCo | Pratique individuelle |
| 14 h 40 | 15 min | 3.2 Documenter l'existant | Démo |
| 14 h 55 | 30 min | 4.1 Générer et modifier du SQL / Python / dbt | Exposé + démo |
| 15 h 25 | 15 min | Pause | |
| 15 h 40 | 50 min | **Exercice 2.2** — Migrer une requête Snowflake en modèle dbt | Binômes |
| 16 h 30 | 15 min | 4.2 Optimiser du code existant | Démo |
| 16 h 45 | 35 min | **Exercice 2.3** — Optimiser le rapport historique | Individuel |
| 17 h 20 | 10 min | Synthèse et préparation J3 | Échange |

---

## 13 h 30 — Retour sur J1 (10 min)

Projeter le `CLAUDE.md` d'un volontaire, le comparer au corrigé. Question à la salle : « quels pièges métier `/init` avait-il ratés ? »
Réponse attendue : le format des montants, les versions multiples de commandes, les paiements fractionnés. Ils reviendront.

---

## 13 h 40 — 3.1 Explorer un dépôt inconnu (25 min)

### Messages clés

Situation typique du consultant : arrivée en mission, un dépôt de 300 modèles dbt et 40 scripts Python, aucune documentation à jour, 2 jours pour être opérationnel.
Claude Code est particulièrement fort sur ce cas : il lit vite, recoupe les fichiers et répond à des questions précises.

Démarche en entonnoir :

1. **Vue d'ensemble** : « explique l'architecture de ce dépôt : couches, flux de données, technologies, points d'entrée ».
2. **Flux de données** : « trace le chemin d'une commande depuis le CSV brut jusqu'à `fct_orders`, fichier par fichier ».
3. **Dépendances** : « quelles dépendances Python sont réellement importées ? lesquelles sont déclarées mais inutilisées ? », « quels modèles dbt dépendent de `stg_orders` ? ».
4. **Questions ciblées** : « où sont gérées les devises ? », « qu'est-ce qui se passe si un montant est vide ? ».
5. **Zones de risque** : « quelles parties du code te semblent fragiles ou incohérentes ? cite les lignes ».

Bonnes pratiques :
- rester en Plan Mode ou en mode `default` : on explore, on ne modifie rien ;
- **faire citer les fichiers et les lignes**, et vérifier soi-même 1 ou 2 affirmations : Claude peut se tromper sur un détail ;
- pour un gros dépôt, demander l'usage d'un subagent d'exploration (« utilise des subagents pour explorer en parallèle les dossiers staging et marts ») : le détail des lectures reste hors de la conversation principale, seul le résumé revient ;
- s'appuyer sur les outils natifs : `dbt ls --select +fct_orders`, `dbt docs generate` (le `manifest.json` contient le lignage complet), `git log --stat` pour savoir ce qui bouge.

### Démo (10 min)

```text
explique-moi le lignage de fct_orders : sources, modèles intermédiaires, tests. Appuie-toi sur dbt ls
et sur les fichiers SQL, et cite les fichiers.
```

Puis :

```text
git log ne contient qu'un commit, donc pas d'historique : à la seule lecture du code, quelles sont les 3 zones
les plus risquées du projet ? ne modifie rien.
```

Selon le tirage, Claude repère souvent la jointure sur les paiements ou le dédoublonnage. **Ne pas valider ni corriger maintenant** : « on note, on y revient en J3 ».

---

## 14 h 05 — Exercice 2.1 : cartographier RetailCo (35 min)

Livrable : un fichier `docs/ARCHITECTURE.md` généré avec Claude, contenant un schéma Mermaid du flux, la liste des modèles et leurs grains, les dépendances, et une section « questions ouvertes ».
Critère de réussite : un nouvel arrivant comprend le projet en 5 minutes de lecture, et **chaque affirmation a été vérifiée** (cocher dans le document).

---

## 14 h 40 — 3.2 Documenter l'existant (15 min)

Trois niveaux de documentation, du plus au moins durable :

| Niveau | Exemple | Prompt type |
| --- | --- | --- |
| Dans le code | Docstrings, commentaires sur les règles métier | « ajoute des docstrings en français aux fonctions publiques de `transform.py`, sans changer le code » |
| Dans dbt | `description` des modèles et colonnes dans les YAML | « complète les descriptions de `_staging.yml` à partir du SQL ; signale ce que tu ne peux pas déduire » |
| Dans le dépôt | `ARCHITECTURE.md`, `README` | (exercice 2.1) |

Message clé : **la documentation générée décrit ce que fait le code, pas ce qu'il devrait faire**. Si le code est faux (c'est le cas ici), la doc décrira fidèlement le bug.
Toujours demander une section « hypothèses et points à valider avec le métier ».

---

## 14 h 55 — 4.1 Générer et modifier du SQL, du Python et du dbt (30 min)

### Messages clés

- **Donner le dialecte et la cible** : « SQL Snowflake », « compatible DuckDB et Snowflake via les macros du projet ».
- **Donner le grain** avant toute requête : « une ligne par client et par mois ».
- **Donner les noms réels** : laisser Claude lire les modèles existants plutôt que décrire les colonnes de mémoire.
- **Exiger la vérification** : « compile avec `dbt compile`, puis `dbt build --select modele+` et corrige jusqu'à ce que tout passe ».
- **Petits pas** : staging d'abord, mart ensuite ; un modèle à la fois.

Spécificités Snowflake à rappeler (et à faire figurer dans `CLAUDE.md` chez le client) :

| Sujet | À préciser dans le prompt |
| --- | --- |
| Dédoublonnage | `QUALIFY ROW_NUMBER() OVER (...) = 1` (DuckDB le supporte aussi) |
| Conversion tolérante | `TRY_TO_NUMBER`, `TRY_TO_DATE` (Snowflake) vs `TRY_CAST` (DuckDB) → macro |
| Semi-structuré | `VARIANT`, `:champ::type`, `LATERAL FLATTEN` |
| Incrémental | `materialized='incremental'`, `unique_key`, `incremental_strategy='merge'`, filtre `is_incremental()` |
| Coût | Taille d'entrepôt, `AUTO_SUSPEND`, éviter les `SELECT *` sur de grosses tables, profil de requête |

### Démo (15 min) : un modèle dbt de A à Z

En direct, en mode `default` pour que la salle voie chaque action :

```text
Crée un modèle dbt marts/fct_daily_sales : une ligne par jour et par canal (channel), avec nombre de commandes
non annulées et chiffre d'affaires. Pars de stg_orders. Ajoute les tests unique sur la combinaison jour+canal
(test singulier ou dbt_utils si disponible, sinon test singulier), documente le grain, puis lance
dbt build --select fct_daily_sales et corrige jusqu'à ce que tout passe.
```

Commenter : Claude lit `stg_orders`, la macro `parse_amount`, le `dbt_project.yml` ; il **découvre** que `dbt_utils` n'est pas installé et s'adapte ; il exécute et corrige.
Montrer le diff final (`git diff`) : **c'est la relecture humaine qui valide**, pas le « tests OK ».

---

## 15 h 40 — Exercice 2.2 : migrer une requête Snowflake en dbt (50 min, binômes)

La requête [`sql/legacy/customer_ltv.sql`](../sql/legacy/customer_ltv.sql) (valeur vie client, LTV — Lifetime Value) doit devenir un modèle `marts/dim_customers.sql`.
Démarche imposée : explorer et lister les problèmes de la requête (Plan Mode) → valider le plan en binôme → implémenter → `dbt build` → comparer les chiffres avec l'ancienne logique et **expliquer chaque écart**.

### Notes formateur

- Problèmes à faire émerger : 5 sous-requêtes corrélées sur la même table, `nb_orders` incluant les annulées alors que `total_revenue` les exclut, `total_paid` gonflé par les versions multiples de commandes, `REPLACE(',', '.')` qui ne gère pas `1 234,50`, filtre `segment IN (...)` inutile (toutes les valeurs y sont), `DATEDIFF` non portable.
- **Piège volontaire** : la plupart des binômes construiront `dim_customers` sur `fct_orders`, qui contient le bug de fan-out. Leur `total_paid` sera faux et le test `unique_fct_orders_order_id` reste rouge. Si un binôme le repère : bravo, mais on corrige en J3.
  Si personne ne le repère, poser la question au débrief : « votre `dbt build` est-il entièrement vert ? ».
- Corrigé : [`solutions/dbt_project/models/marts/dim_customers.sql`](../solutions/dbt_project/models/marts/dim_customers.sql) (s'appuie sur le `fct_orders` corrigé).
- 🚀 Pour les rapides : rendre `fct_orders` incrémental (`merge` sur `order_id`, filtre sur `updated_at`).

---

## 16 h 30 — 4.2 Optimiser du code existant (15 min)

### Messages clés

Une optimisation est une **refactorisation à comportement constant**. Méthode en 4 temps, à imposer à Claude :

1. **Mesurer** l'existant (temps, mémoire) et **figer le résultat** de référence (fichier CSV ou test de caractérisation) ;
2. **Diagnostiquer** : où passe le temps ? (`iterrows`, filtres répétés dans une boucle, `apply(axis=1)`, N requêtes au lieu d'une) ;
3. **Réécrire** : vectorisation pandas, jointures, ou déléguer au moteur SQL (DuckDB localement, Snowflake en production) ;
4. **Prouver** que le résultat est identique (comparaison automatique) et mesurer le gain.

Le piège classique : la version « optimisée » corrige au passage un comportement de l'ancienne (ex. quelle occurrence d'une commande en double est utilisée) et **les chiffres changent sans que personne ne le décide**. Toute divergence doit être explicitée et validée.

---

## 16 h 45 — Exercice 2.3 : optimiser le rapport historique (35 min)

[`src/retail_pipeline/legacy_report.py`](../src/retail_pipeline/legacy_report.py) met environ **90 secondes** sur le jeu de formation.
Objectif : moins d'une seconde, résultat **strictement identique**, code typé et testé.

### Notes formateur

- Prévenir : lancer l'ancien rapport une seule fois et sauvegarder sa sortie (sinon on perd 90 s à chaque comparaison). Bon réflexe à faire formuler par Claude.
- Point subtil : l'historique prend la **première occurrence** d'une commande dans le fichier (`iloc[0]`), pas la plus récente. Une version « propre » qui dédoublonne sur `updated_at` donne des chiffres différents. Bonne discussion : on reproduit d'abord, on corrige ensuite, en le disant.
- Corrigé : [`solutions/src/retail_pipeline/monthly_report.py`](../solutions/src/retail_pipeline/monthly_report.py) (DuckDB, ≈ 0,2 s, écart nul sur les 84 lignes).

---

## 17 h 20 — Synthèse (10 min)

1. Explorer avant de produire, faire citer les sources, vérifier.
2. Grain, dialecte, critère de vérification dans chaque demande de code.
3. Optimiser = mesurer, figer, réécrire, prouver.

**Question ouverte pour J3** : « nos tests passent tous… nos chiffres sont-ils justes pour autant ? »
