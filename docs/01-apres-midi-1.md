# Après-midi 1 — Prendre en main Claude Code

**Thèmes couverts** : 1. Introduction et fondamentaux · 2. Prompting & context engineering
**Exercices participants** : [`exercises/J1_prise_en_main.md`](../exercises/J1_prise_en_main.md)

| Horaire | Durée | Séquence | Format |
| --- | --- | --- | --- |
| 13 h 30 | 15 min | Accueil, tour de table, attentes | Échange |
| 13 h 45 | 35 min | 1.1 De l'assistant conversationnel à l'agent | Exposé + démo |
| 14 h 20 | 30 min | 1.2 Installation, configuration, permissions | Démo + pratique |
| 14 h 50 | 30 min | **Exercice 1.1** — Premier contact avec RetailCo | Pratique individuelle |
| 15 h 20 | 15 min | Pause | |
| 15 h 35 | 30 min | 2.1 Formuler des instructions efficaces | Exposé + **Exercice 1.2** |
| 16 h 05 | 25 min | 2.2 Le contexte : fenêtre, `CLAUDE.md`, mémoire | Exposé + démo |
| 16 h 30 | 30 min | **Exercice 1.3** — Écrire le `CLAUDE.md` du projet | Pratique |
| 17 h 00 | 20 min | 2.3 Plan Mode et décomposition + **Exercice 1.4** | Démo + pratique |
| 17 h 20 | 10 min | Synthèse, questions, préparation J2 | Échange |

---

## 13 h 30 — Accueil (15 min)

Tour de table en une phrase : rôle, stack habituelle (SQL/dbt/Python/Spark…), usage actuel de l'IA (aucun / ChatGPT / Copilot / Cursor / Claude Code).
Noter au tableau les profils « déjà utilisateurs » : ils serviront de binômes référents.

Poser le cadre : 50 % de pratique, un projet fil rouge, on casse des choses volontairement, on ne travaille jamais sur des données client réelles pendant la formation.

---

## 13 h 45 — 1.1 De l'assistant conversationnel à l'agent (35 min)

### Messages clés

**Un LLM (Large Language Model) en mode conversationnel** reçoit du texte et renvoie du texte. C'est vous qui copiez le code, l'exécutez, recollez l'erreur.
**Un agent** reçoit un objectif, puis **boucle** : il collecte du contexte, agit avec des outils, vérifie le résultat, et recommence jusqu'à ce que l'objectif soit atteint (ou qu'il ait besoin de vous).

```
            ┌──────────────────────────────────────────┐
 objectif → │ 1. Collecter le contexte (lire, chercher) │
            │ 2. Agir (éditer, exécuter une commande)   │ ← vous pouvez interrompre (Échap)
            │ 3. Vérifier (tests, sortie, erreurs)      │   et réorienter à tout moment
            └──────────────┬───────────────────────────┘
                           └── boucle jusqu'à « terminé » ou question à l'humain
```

| | Assistant conversationnel (chat) | Agent (Claude Code) |
| --- | --- | --- |
| Accès au code | Ce que vous collez | Tout le dépôt, à la demande |
| Exécution | Aucune | Commandes shell, tests, dbt, git |
| Vérification | Par vous | Par lui-même, si vous lui en donnez les moyens |
| Unité de travail | Une réponse | Une tâche (plusieurs dizaines d'actions) |
| Risque principal | Réponse fausse | **Action** fausse (fichier écrasé, commande dangereuse) |
| Votre rôle | Rédacteur de questions | **Chef de projet + relecteur** |

**Les outils de Claude Code** (à montrer en démo, sans entrer dans le détail) : lecture de fichiers, recherche (`Grep`, `Glob`), édition (`Edit`, `Write`), exécution (`Bash`), web (`WebFetch`, `WebSearch`), délégation à des subagents, et toutes les extensions (MCP, skills) vues en J3.

**Où s'utilise Claude Code** : terminal (le cœur de la formation), extensions VS Code et JetBrains, application de bureau, web (claude.ai/code), Slack, GitHub Actions / GitLab CI. Même moteur, mêmes fichiers de configuration.

### Démo (10 min)

Dans le dépôt RetailCo, mode par défaut, prompt projeté :

```text
que fait ce projet ? donne-moi l'architecture en 5 lignes et la commande pour tout lancer
```

Commenter en direct : **Claude n'a rien reçu à part la question** ; il décide seul de lire le README, `pyproject.toml`, de lister `src/`. Montrer les appels d'outils affichés.

Puis :

```text
lance les tests unitaires et dis-moi s'ils passent
```

Claude demande la permission d'exécuter `pytest` (ou non, si la règle `allow` du projet le couvre — l'occasion d'annoncer la partie permissions).

### Notes formateur

- Question fréquente : « quel modèle tourne derrière ? » → `/model` permet de choisir (Opus pour le raisonnement complexe, Sonnet par défaut pour la plupart des tâches de code, Haiku pour les tâches simples et rapides). On en reparle côté coûts en J4.
- Ne pas promettre que l'agent « comprend » le métier : il infère à partir de ce qu'il lit. D'où l'importance de `CLAUDE.md` (après la pause).

---

## 14 h 20 — 1.2 Installation, configuration, permissions (30 min)

### Installation (rappel : normalement faite en amont)

```bash
# macOS, Linux, WSL (installation native recommandée, mises à jour automatiques)
curl -fsSL https://claude.ai/install.sh | bash
# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
# Alternatives : brew install --cask claude-code   |   winget install Anthropic.ClaudeCode
claude --version
```

Sur Windows natif, Git for Windows est recommandé (sinon Claude Code utilise PowerShell comme shell). WSL n'en a pas besoin.

Connexion au premier lancement de `claude` : compte Claude (Pro, Max, Team, Enterprise), Claude Console (API), ou fournisseur cloud (Amazon Bedrock, Google Cloud, Microsoft Foundry).

### Commandes essentielles (sur l'aide-mémoire)

| Commande | Effet |
| --- | --- |
| `claude` / `claude "tâche"` | Session interactive (avec un premier prompt) |
| `claude -p "question"` | Mode non interactif (*headless*) : répond puis sort — base de l'automatisation (J3/J4) |
| `claude -c` / `claude -r` | Reprendre la dernière conversation / choisir une conversation |
| `/help`, `/` | Liste des commandes et skills disponibles |
| `/clear` | Repartir d'un contexte vide |
| `/model`, `/effort` | Choisir le modèle et le niveau de réflexion |
| `/usage`, `/context` | Consommation et occupation de la fenêtre de contexte |
| `Échap` | Interrompre Claude ; `Échap` ×2 ou `/rewind` : revenir à un point de sauvegarde |
| `Maj+Tab` | Faire défiler les modes de permission |
| `@chemin/fichier` | Référencer un fichier dans le prompt |
| `!commande` | Exécuter une commande shell soi-même |

### Les modes de permission

| Mode | Ce qui s'exécute sans demander | Usage |
| --- | --- | --- |
| `default` (« Manual ») | Lectures uniquement | Découverte, code client sensible — **mode de la formation** |
| `acceptEdits` | Lectures + éditions de fichiers + commandes de fichiers courantes dans le dossier | Itérer sur du code que l'on relit au fil de l'eau |
| `plan` | Lectures (exploration), aucune modification | Analyser et planifier avant de toucher au code |
| `auto` | Tout, avec un classifieur de sécurité en arrière-plan | Tâches longues, si disponible et autorisé |
| `dontAsk` | Lectures + outils pré-approuvés ; tout le reste est refusé | CI et scripts verrouillés |
| `bypassPermissions` | Tout | **Uniquement** dans un conteneur ou une VM (machine virtuelle) isolé(e) |

Points à souligner :
- Les règles `deny` s'appliquent **dans tous les modes**, y compris `bypassPermissions`.
- Les écritures dans `.git`, `.claude`, `.mcp.json`… ne sont jamais auto-approuvées (sauf `bypassPermissions`).

### Démo : les fichiers de configuration du dépôt

Ouvrir [`.claude/settings.json`](../.claude/settings.json) et le lire avec la salle :

- `allow` : pytest, ruff, dbt en local, git en lecture → pas de friction sur les actions sûres ;
- `ask` : `git commit`, `git push`, dbt sur la cible Snowflake → confirmation humaine ;
- `deny` : lecture de `.env` et des profils d'identifiants, modification de `data/raw/`, `curl`/`wget`.

Ordre de priorité des réglages : **managed** (imposé par l'IT) > ligne de commande > `.claude/settings.local.json` (personnel, non commité) > `.claude/settings.json` (équipe, commité) > `~/.claude/settings.json` (utilisateur).

Démonstration en direct : `lis le fichier .env` → refus. C'est la première brique de la partie sécurité (J4).

---

## 14 h 50 — Exercice 1.1 : premier contact avec RetailCo (30 min)

Voir l'énoncé. Objectif : que **chacun** ait une session fonctionnelle, ait vu Claude lire, exécuter et répondre, et ait rencontré une demande de permission.

Tour de salle : débloquer les installations ratées en priorité. Au bout de 20 min, faire partager 2 ou 3 réponses à « qu'est-ce qui vous a surpris ? ».

---

## 15 h 35 — 2.1 Formuler des instructions efficaces (30 min)

### Messages clés

Un bon prompt pour un agent n'est pas une incantation, c'est **un bon ticket Jira** : contexte, objectif, contraintes, critère de fin.

| Principe | Mauvais | Bon |
| --- | --- | --- |
| Être spécifique | « corrige le bug » | « dans `transform.clean_orders`, les commandes en double gardent l'ancienne version : garde celle qui a le `updated_at` le plus récent » |
| Pointer les fichiers | « regarde le modèle des commandes » | « regarde `@dbt_project/models/marts/fct_orders.sql` » |
| Donner un critère de vérification | « ajoute des tests » | « ajoute un test qui échoue sur le code actuel, puis corrige, puis lance `pytest -q` jusqu'à ce que tout passe » |
| Fixer les contraintes | — | « sans ajouter de dépendance », « SQL compatible Snowflake et DuckDB », « ne modifie pas l'API publique » |
| Donner un exemple | « formate les montants » | « `'1 234,50'` → `1234.5`, `''` → `None` » |
| Une tâche à la fois | « refais le pipeline et la doc et les tests » | trois demandes successives, avec vérification entre chaque |
| Laisser explorer d'abord | « implémente X » | « lis le code concerné et explique-moi comment X devrait s'insérer, ne modifie rien » |

Formule à mémoriser : **Contexte → Objectif → Contraintes → Vérification**.

Autres leviers :
- coller une erreur complète ou une capture d'écran plutôt que la paraphraser ;
- demander à Claude de **poser des questions** avant de commencer quand le besoin est flou (« interroge-moi sur ce qui manque ») ;
- corriger tôt : `Échap` dès que la direction est mauvaise, plutôt que de laisser finir.

### Exercice 1.2 (15 min, intégré)

Les participants réécrivent 3 prompts faibles de l'énoncé, les testent, et comparent le nombre d'actions et la qualité du résultat. Débrief : faire lire à voix haute le meilleur prompt de la salle.

---

## 16 h 05 — 2.2 Le contexte : fenêtre, `CLAUDE.md`, mémoire (25 min)

### La fenêtre de contexte

Tout ce que Claude « sait » pendant une session tient dans sa fenêtre de contexte : instructions système, `CLAUDE.md`, historique, contenu des fichiers lus, sorties de commandes. Elle est grande, mais :
- plus elle est remplie, plus le coût de chaque échange augmente (tout est renvoyé à chaque requête) ;
- des informations anciennes et hors-sujet diluent l'attention.

Gestes à adopter :

| Geste | Quand |
| --- | --- |
| `/context` | Voir ce qui occupe la fenêtre |
| `/clear` | Entre deux tâches sans rapport (gratuit) — `/rename` avant pour retrouver la session |
| `/compact consigne` | Résumer une longue session en gardant l'essentiel (ex. `/compact garde les fichiers modifiés et les résultats de tests`) |
| Subagents | Déléguer les tâches verbeuses (recherche, logs) : seul le résumé revient (J3) |

### `CLAUDE.md` : la mémoire du projet

Chaque session démarre vierge. `CLAUDE.md` est un fichier Markdown **chargé automatiquement au démarrage** qui donne les instructions permanentes.

| Emplacement | Portée | Commité ? |
| --- | --- | --- |
| Politique d'entreprise (`/etc/claude-code/CLAUDE.md` sous Linux…) | Toute l'organisation, imposé par l'IT | — |
| `~/.claude/CLAUDE.md` | Vous, tous vos projets | Non |
| `./CLAUDE.md` (ou `./.claude/CLAUDE.md`) | Le projet, toute l'équipe | **Oui** |
| `./CLAUDE.local.md` | Vous, ce projet (à mettre dans `.gitignore`) | Non |
| `sous-dossier/CLAUDE.md` | Chargé quand Claude travaille dans ce sous-dossier | Oui |
| `.claude/rules/*.md` avec `paths:` | Chargé seulement pour les fichiers correspondants | Oui |

Tous les fichiers trouvés sont **concaténés** (pas de remplacement). Un fichier peut en importer un autre avec `@chemin/fichier`.
Il existe aussi une **mémoire automatique** que Claude écrit lui-même à partir de vos corrections ; `/memory` permet de consulter et éditer l'ensemble.

**Ce qui va dans `CLAUDE.md`** : ce que Claude ne peut pas deviner en lisant le code.
- commandes de build/test exactes ;
- pièges métier (« les montants arrivent au format français », « une commande peut avoir 2 paiements ») ;
- conventions d'équipe (nommage dbt, format de commit) ;
- interdits (« ne jamais lancer dbt sur la prod »).

**Ce qui n'y va pas** : la description de chaque fichier (Claude sait lire), des procédures longues et rares (→ skills, J3), des règles qui doivent être **garanties** (→ permissions `deny` ou hooks : `CLAUDE.md` est un contexte, pas une contrainte).
Viser **moins de 200 lignes** ; au-delà, l'adhésion baisse et le coût augmente.

### Démo (5 min)

Montrer [`.claude/rules/dbt.md`](../.claude/rules/dbt.md) : grâce à `paths:`, ces règles n'entrent dans le contexte que quand Claude touche un fichier dbt.

---

## 16 h 30 — Exercice 1.3 : écrire le `CLAUDE.md` du projet (30 min)

1. `/init` génère une première version à partir du code.
2. Les participants la critiquent et l'enrichissent avec les **pièges métier** qu'ils ont découverts (ou qu'ils trouvent en interrogeant Claude sur les données).
3. Test : `/clear`, puis une question piège (« comment est calculé le montant en euros ? ») pour vérifier que le contexte est utilisé.

Corrigé de référence : [`solutions/CLAUDE.md`](../solutions/CLAUDE.md). **Ne pas le montrer avant la fin** : l'intérêt est de constater que `/init` ne trouve pas seul les pièges métier.
Les pièges listés dans le corrigé seront exactement les bugs chassés en J3 : c'est voulu, on y reviendra.

---

## 17 h 00 — 2.3 Plan Mode et décomposition (20 min)

### Messages clés

Le Plan Mode (`Maj+Tab` jusqu'à « plan », ou `claude --permission-mode plan`) : Claude **explore et propose un plan sans rien modifier**. Vous validez, amendez ou rejetez avant toute écriture.

Workflow recommandé pour toute tâche non triviale : **Explorer → Planifier → Implémenter → Vérifier → Commiter**.

- Explorer : « lis X et Y, explique-moi comment ça marche, ne modifie rien ».
- Planifier : Plan Mode, plan en étapes avec fichiers impactés et tests prévus. Ajouter « pense en profondeur » pour les sujets complexes.
- Implémenter : sortir du Plan Mode, étape par étape, vérifier après chaque étape.
- Vérifier : tests, `dbt build`, relecture du diff.

Décomposer : une tâche = un résultat vérifiable. Un plan de 15 étapes se découpe en 3 sessions avec `/clear` entre elles, le plan étant sauvegardé dans un fichier (`PLAN.md`).

### Exercice 1.4 (15 min)

Ajouter au pipeline une option `--since AAAA-MM-JJ` qui ne charge que les commandes postérieures à une date. **Plan Mode obligatoire**, et le plan doit être validé par le binôme avant implémentation.

---

## 17 h 20 — Synthèse (10 min)

Faire formuler par la salle les 3 idées retenues. Compléter avec :
1. l'agent agit → permissions et relecture ;
2. contexte = qualité et coût → `CLAUDE.md` court, `/clear` souvent ;
3. Plan Mode avant de coder.

**Pour J2** : garder son `CLAUDE.md` ; ceux qui le souhaitent lisent la requête [`sql/legacy/customer_ltv.sql`](../sql/legacy/customer_ltv.sql) (sans Claude !) et notent ce qu'ils y trouvent suspect.
