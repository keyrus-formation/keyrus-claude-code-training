# Après-midi 3 — Fiabiliser et outiller

**Thèmes couverts** : 5. Testing, debugging & qualité · 6. Intégrations et automatisation
**Exercices participants** : [`exercises/J3_testing_debugging_integrations.md`](../exercises/J3_testing_debugging_integrations.md)

| Horaire | Durée | Séquence | Format |
| --- | --- | --- | --- |
| 13 h 30 | 20 min | 5.1 Tester avec un agent : « test d'abord » | Exposé |
| 13 h 50 | 55 min | **Exercice 3.1** — La chasse aux 4 bugs | Individuel, débrief collectif |
| 14 h 45 | 15 min | 5.2 Qualité de données et validation du code généré | Exposé |
| 15 h 00 | 25 min | **Exercice 3.2** — Contrôles de qualité Python + dbt | Pratique |
| 15 h 25 | 15 min | Pause | |
| 15 h 40 | 25 min | 6.1 Étendre Claude Code : la boîte à outils | Exposé |
| 16 h 05 | 25 min | 6.2 MCP et connexions aux outils Data | Démo + **Exercice 3.3** |
| 16 h 30 | 40 min | 6.3 Skills, hooks, automatisation + **Exercice 3.4** | Démo + pratique |
| 17 h 10 | 20 min | Synthèse et préparation J4 | Échange |

---

## 13 h 30 — 5.1 Tester avec un agent (20 min)

### Messages clés

Rappel de la question laissée en fin de J2 : **les 4 tests Python passent, et pourtant le pipeline perd de l'argent**.
Une suite verte ne prouve que ce qu'elle teste. Et un agent qui écrit du code *et* ses tests peut écrire des tests qui valident ses propres erreurs.

Règles du jeu avec Claude Code :

1. **Test d'abord (TDD — Test-Driven Development)** : « écris un test qui reproduit le bug, montre-moi qu'il échoue, *ensuite* corrige ». Un test qui n'a jamais échoué n'a rien prouvé.
2. **Les cas limites viennent de vous** : formats français, valeurs vides, doublons, devises, fuseaux horaires, paiements fractionnés. Claude en propose, vous complétez avec la connaissance du métier.
3. **Ne jamais laisser modifier un test pour le faire passer** sans le décider explicitement. À écrire dans `CLAUDE.md` : « ne modifie jamais un test existant pour le faire passer ; signale-le ».
4. **Interdire les comportements de contournement** : `try/except: pass`, `errors="coerce"` silencieux, `DISTINCT` qui masque une jointure fausse.
5. **Relire le diff** : la relecture humaine reste la dernière ligne de défense. Pour un regard neuf, déléguer la relecture à un subagent qui n'a pas vu la conversation (le dépôt en fournit un : `data-reviewer`).

### Le debugging en 4 temps

| Étape | Prompt type |
| --- | --- |
| Reproduire | « voici le symptôme : … Écris le plus petit script ou test qui le reproduit » |
| Localiser | « trouve la cause racine, pas le symptôme ; explique-la avant de proposer un correctif » |
| Corriger | « corrige uniquement la cause, sans changement hors sujet » |
| Prouver | « le test de reproduction passe, toute la suite passe, et voici l'impact chiffré sur les données » |

Fournir les éléments bruts : message d'erreur complet, sortie de `dbt build`, échantillon de lignes. Ne pas paraphraser.

---

## 13 h 50 — Exercice 3.1 : la chasse aux 4 bugs (55 min)

Énoncé : le métier signale que « le chiffre d'affaires ne colle pas avec la comptabilité ». Les participants disposent de Claude Code, du `dbt build` rouge et de leur `CLAUDE.md`.
Pour chaque bug trouvé : un test qui échoue, le correctif, l'impact chiffré.

### Les 4 bugs (feuille formateur, ne pas distribuer)

| # | Où | Bug | Impact sur le jeu de formation | Symptôme observable |
| --- | --- | --- | --- | --- |
| B1 | `transform.parse_amount` | `'1 234,50'` → l'espace des milliers n'est pas retiré → `ValueError` avalée → `None` | **366 commandes** sans montant, ≈ **572 k€** de CA ignoré | Les montants ≥ 1 000 € au format français disparaissent |
| B2 | `transform.clean_orders` | Tri croissant + `keep="first"` → garde la **plus ancienne** version de la commande | **1 000 commandes** avec un statut périmé (retours non vus) | Taux de retour sous-estimé |
| B3 | `transform.clean_orders` | Division par le taux au lieu de multiplication (`FX_TO_EUR` = valeur d'une unité en EUR) | **4 058 commandes** en USD/CHF mal converties | 100 USD → 108,70 € au lieu de 92 € |
| B4 | `fct_orders.sql` et `build_order_facts` | Jointure directe sur `payments` (2 paiements pour certaines commandes) → *fan-out* | **2 796 lignes** en double dans `fct_orders`, CA gonflé d'≈ **901 k€** | Test dbt `unique_fct_orders_order_id` en échec |

Indices progressifs si un participant bloque (toutes les 15 min) :
1. « Comparez `count(*)` et `count(distinct order_id)` dans `fct_orders`. »
2. « Combien de montants non vides deviennent `None` après `parse_amount` ? »
3. « Prenez une commande présente 2 fois dans `orders.csv` : quel statut garde le pipeline ? »
4. « 100 USD, c'est combien en euros ? »

### Débrief (10 min)

- Combien de bugs trouvés ? Lequel a été trouvé par Claude spontanément, lequel grâce à une question métier ? (En général B4 est trouvé vite grâce au test dbt rouge ; B1 et B3 grâce au `CLAUDE.md` enrichi en J1 ; B2 est le plus souvent raté.)
- Montrer que les pièges du corrigé de `CLAUDE.md` correspondent exactement aux bugs : **le contexte métier est ce qui permet à l'agent de trouver les bugs métier**.
- Corrigés : [`solutions/src/retail_pipeline/transform.py`](../solutions/src/retail_pipeline/transform.py), [`solutions/tests/test_regressions.py`](../solutions/tests/test_regressions.py) (9 tests dont 6 échouent sur le code d'origine), [`solutions/dbt_project/models/marts/fct_orders.sql`](../solutions/dbt_project/models/marts/fct_orders.sql).

---

## 14 h 45 — 5.2 Qualité de données et validation du code généré (15 min)

### Deux types de tests, deux moments

| | Tests unitaires (pytest) | Tests de données (dbt tests, contrôles Python) |
| --- | --- | --- |
| Vérifient | Que le **code** fait ce qu'on attend sur des cas construits | Que les **données** respectent les règles à chaque exécution |
| Exemples | `parse_amount('1 234,50') == 1234.5` | `unique`, `not_null`, `accepted_values`, `relationships`, rapprochement paiements/commandes |
| Quand | À chaque modification (CI) | À chaque chargement (pipeline, `dbt build`) |

Contrôles qui détectent des anomalies **dans la source** (à signaler, pas à corriger en silence) : 209 montants négatifs, 87 commandes datées de 2031, 212 montants vides, 2 % de clients en double, emails en majuscules.

### Valider du code généré : la check-list

1. Les tests existants passent, **et** un test nouveau couvre le changement.
2. Le diff ne touche que ce qui était demandé.
3. Les chiffres clés sont réconciliés avec une source indépendante (nombre de lignes, sommes de contrôle).
4. Pas de comportement silencieux ajouté (exception avalée, valeur par défaut masquante).
5. Relecture par un humain, idéalement aidée par une relecture indépendante (subagent `data-reviewer`, voir J4).

---

## 15 h 00 — Exercice 3.2 : contrôles de qualité (25 min)

Compléter `quality.py` (4 fonctions TODO) et ajouter les tests dbt manquants, dont un test singulier de rapprochement paiements/commandes.
Corrigés : [`solutions/src/retail_pipeline/quality.py`](../solutions/src/retail_pipeline/quality.py), [`solutions/dbt_project/tests/assert_payments_reconcile_with_orders.sql`](../solutions/dbt_project/tests/assert_payments_reconcile_with_orders.sql).

---

## 15 h 40 — 6.1 Étendre Claude Code : la boîte à outils (25 min)

| Brique | Ce que c'est | Chargé quand | Exemple RetailCo |
| --- | --- | --- | --- |
| `CLAUDE.md` / rules | Instructions permanentes | Toujours (rules : selon les fichiers) | Pièges métier, conventions |
| **Skill** | Procédure réutilisable (`.claude/skills/<nom>/SKILL.md` + fichiers annexes), invocable par `/nom` ou chargée automatiquement si sa description correspond | À la demande | `/dbt-model`, `/sql-review`, `/data-quality-audit` |
| **Subagent** | Assistant spécialisé avec son propre contexte, ses outils, son modèle (`.claude/agents/<nom>.md`) | Quand Claude délègue ou qu'on le demande | `data-reviewer` (lecture seule, Sonnet) |
| **Hook** | Commande shell exécutée **de façon déterministe** à un moment du cycle (avant/après un outil, fin de tâche…) | À chaque événement | Formatage `ruff`, blocage des secrets et du SQL destructeur |
| **MCP** (Model Context Protocol) | Protocole standard pour brancher des outils externes (bases, dbt, Jira, GitHub…) | Outils chargés à la demande | Serveur MCP dbt, serveur MCP géré par Snowflake |
| **Plugin** | Paquet qui regroupe skills, agents, hooks, MCP pour les partager | À l'installation | Futur « plugin Keyrus Data » |
| **Mode headless** (`claude -p`) | Claude Code en ligne de commande non interactive | Scripts, CI, tâches planifiées | Rapport de qualité nocturne |

Règle de choix :
- **une consigne à suivre la plupart du temps** → `CLAUDE.md` ;
- **une procédure en plusieurs étapes, occasionnelle** → skill ;
- **une règle qui doit s'appliquer à 100 %** → hook ou permission `deny` ;
- **un travail verbeux ou nécessitant un regard neuf** → subagent ;
- **un système externe** → MCP… ou simplement sa CLI (`gh`, `snow`, `dbt`), souvent plus économe en contexte.

Les anciennes commandes personnalisées (`.claude/commands/*.md`) fonctionnent toujours et sont désormais fusionnées avec les skills.

---

## 16 h 05 — 6.2 MCP et outils Data (25 min)

### Démo : brancher le serveur MCP dbt

Le serveur MCP officiel de dbt Labs (`dbt-mcp`) s'exécute localement avec `uvx` et expose notamment la découverte des modèles, le lignage et l'exécution de commandes dbt.

```bash
claude mcp add dbt \
  -e DBT_PROJECT_DIR="$PWD/dbt_project" -e DBT_PATH="$(which dbt)" -e DBT_PROFILES_DIR="$PWD/dbt_project" \
  -- uvx dbt-mcp
claude mcp list
```

Dans Claude Code : `/mcp` pour voir l'état des serveurs. Puis :

```text
avec le serveur MCP dbt, liste les modèles qui dépendent de stg_orders et leurs tests
```

Portées d'installation : `local` (défaut, vous seul, ce projet), `project` (fichier `.mcp.json` commité, partagé avec l'équipe — chaque membre approuve le serveur au premier usage), `user` (tous vos projets). Modèle de configuration : [`.mcp.json.example`](../.mcp.json.example) (les `${VARIABLES}` sont lues dans l'environnement : aucun secret dans le fichier).

### Snowflake

Snowflake propose un **serveur MCP géré** (objet `MCP SERVER` créé dans le compte) qui expose Cortex Analyst, Cortex Search, des agents Cortex et l'exécution SQL, avec le contrôle d'accès par rôles (RBAC — Role-Based Access Control) de Snowflake. À configurer avec un rôle **en lecture seule** pour l'exploration.
Alternative souvent suffisante : laisser Claude utiliser la CLI Snowflake (`snow sql -q ...`) avec un rôle restreint et une règle `ask` dans les permissions.

### Messages de prudence

- Un serveur MCP **agit avec vos droits** : base de recette, rôle lecture seule, jamais d'identifiants de production.
- Les réponses d'outils MCP entrent dans le contexte : limiter les requêtes qui ramènent des milliers de lignes (Claude Code avertit au-delà de 10 000 tokens de sortie MCP).
- N'installer que des serveurs de sources connues (éditeur officiel, annuaire Anthropic, revue interne).

**Exercice 3.3 (15 min)** : brancher `dbt-mcp`, l'utiliser pour produire la matrice « modèle → tests → colonnes non testées ».

---

## 16 h 30 — 6.3 Skills, hooks et automatisation (40 min)

### Démo skills (10 min)

Ouvrir [`.claude/skills/dbt-model/SKILL.md`](../.claude/skills/dbt-model/SKILL.md). Points à montrer :
- le `description` (c'est lui qui déclenche le chargement automatique) ;
- `$ARGUMENTS`, `allowed-tools` (outils pré-autorisés pendant l'exécution du skill) ;
- [`sql-review`](../.claude/skills/sql-review/SKILL.md) : `disable-model-invocation: true` (seulement par `/sql-review`) et l'injection d'une commande `` !`git diff ...` `` exécutée avant que Claude lise le skill ;
- [`data-quality-audit`](../.claude/skills/data-quality-audit/SKILL.md) : `context: fork` + `agent: Explore` → s'exécute dans un subagent en lecture seule, seul le rapport revient.

Lancer `/data-quality-audit data/raw/orders.csv` et comparer avec les anomalies trouvées à la main en 3.2.

### Démo hooks (10 min)

Ouvrir [`.claude/settings.json`](../.claude/settings.json) et les scripts de [`.claude/hooks/`](../.claude/hooks) :

| Hook | Événement | Effet |
| --- | --- | --- |
| `protect-files.sh` | `PreToolUse` sur `Edit|Write` | Bloque toute écriture dans `.env`, `data/raw/`, `.git/`, `profiles.yml` |
| `block-destructive-sql.sh` | `PreToolUse` sur `Bash` | Bloque `rm -rf`, `DROP/TRUNCATE TABLE`, `DELETE` sans `WHERE`, dbt sur `prod` |
| `format-python.sh` | `PostToolUse` sur `Edit|Write` | `ruff format` + `ruff check --fix` ; renvoie les erreurs restantes à Claude |

Mécanique : le hook reçoit en JSON (entrée standard) la description de l'action ; **code de sortie 2 = action bloquée**, le message d'erreur est renvoyé à Claude qui s'adapte.
Démo : « supprime la table raw.orders dans DuckDB » → bloqué ; Claude explique le blocage. `/hooks` liste les hooks actifs.

Message clé : **un hook est une garantie, une instruction dans `CLAUDE.md` est une demande**.

### Automatisation des tâches récurrentes (5 min)

Mode non interactif, pour les scripts, la CI ou une tâche planifiée :

```bash
claude -p "lance /data-quality-audit data/raw/orders.csv et écris le rapport dans reports/qualite.md" \
  --permission-mode dontAsk \
  --allowedTools "Read" "Edit(./reports/**)" "Bash(python *)" \
  --output-format json > run.json
```

`dontAsk` + liste blanche d'outils = rien d'autre ne peut s'exécuter. Cas d'usage consultant : rapport de qualité quotidien, mise à jour de la documentation dbt, triage des échecs de CI, revue automatique des PR (J4).

### Exercice 3.4 (15 min)

Au choix : écrire un skill `/explain-model <modele>` qui documente un modèle dbt (grain, lignage, tests, colonnes non testées), **ou** un hook `Stop` qui lance `pytest -q` à la fin de chaque réponse de Claude et lui renvoie les échecs.

---

## 17 h 10 — Synthèse (20 min)

1. Test d'abord, cas limites métier, relecture du diff.
2. Les données se testent à chaque chargement, le code à chaque modification.
3. CLAUDE.md = demande ; hook/permission = garantie ; skill = procédure ; MCP = connexion ; subagent = contexte séparé.

**Pour J4** : chacun pousse sa branche de corrections sur le dépôt de la session (sans fusionner).
