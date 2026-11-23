# Aide-mémoire Claude Code — consultants Data Keyrus

## Lancer

| Commande | Effet |
| --- | --- |
| `claude` | Session interactive dans le dossier courant |
| `claude "tâche"` | Session avec un premier prompt |
| `claude -p "question"` | Mode non interactif (scripts, CI) — `--output-format json` |
| `claude -c` / `claude -r` | Reprendre la dernière session / en choisir une |
| `claude --permission-mode plan` | Démarrer en Plan Mode |

## Dans la session

| Commande / touche | Effet |
| --- | --- |
| `/` | Commandes et skills disponibles |
| `Maj+Tab` | Changer de mode : `default` → `acceptEdits` → `plan` (→ `auto` si disponible) |
| `Échap` | Interrompre ; `Échap` ×2 ou `/rewind` : revenir à un point de sauvegarde |
| `@fichier` | Mettre un fichier dans le contexte |
| `!commande` | Lancer une commande shell soi-même |
| `/clear` | Contexte vide (entre deux tâches) — `/rename` avant pour retrouver la session |
| `/compact consigne` | Résumer la session en gardant l'essentiel |
| `/context`, `/usage` | Occupation du contexte, consommation et recommandations |
| `/model`, `/effort` | Choisir le modèle, le niveau de réflexion |
| `/init`, `/memory` | Créer ou éditer `CLAUDE.md` et la mémoire |
| `/permissions`, `/hooks`, `/mcp` | Inspecter permissions, hooks, serveurs MCP |
| `/code-review`, `/security-review` | Revue du code / revue de sécurité des changements |

## Bien formuler : Contexte → Objectif → Contraintes → Vérification

> « Dans `@dbt_project/models/marts/fct_orders.sql` (contexte), garantis une ligne par commande (objectif),
> sans changer les colonnes exposées et en SQL portable DuckDB/Snowflake (contraintes). Ajoute un test qui échoue avant
> le correctif, puis lance `dbt build --select fct_orders+` jusqu'à ce que tout passe (vérification). »

## Workflow : Explorer → Planifier → Implémenter → Vérifier → Commiter

## Où mettre quoi

| Besoin | Outil |
| --- | --- |
| Consigne permanente, piège métier | `CLAUDE.md` (< 200 lignes) ; règles ciblées : `.claude/rules/*.md` avec `paths:` |
| Préférence personnelle | `~/.claude/CLAUDE.md`, `CLAUDE.local.md` |
| Procédure réutilisable | Skill : `.claude/skills/<nom>/SKILL.md` → `/nom` |
| Regard neuf, tâche verbeuse | Subagent : `.claude/agents/<nom>.md` |
| Règle à garantir à 100 % | Permission `deny` ou hook (`exit 2` = bloqué) |
| Outil externe (dbt, Snowflake, Jira…) | MCP : `claude mcp add …` — ou la CLI de l'outil |

## Règles d'or en mission

1. Compte **commercial** Keyrus uniquement ; jamais de compte personnel sur du code client.
2. Pas de secrets ni d'identifiants de production sur le poste ; `.env` en `deny`.
3. Exploration avec un rôle **lecture seule** ; agrégats plutôt que lignes de données.
4. Plan Mode avant toute tâche non triviale ; test qui échoue avant tout correctif.
5. Je relis chaque diff ; **je signe ce que je livre**.
6. `/clear` souvent, Sonnet par défaut, prompts précis : le contexte coûte.
