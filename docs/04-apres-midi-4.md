# Après-midi 4 — Industrialiser, sécuriser, livrer

**Thèmes couverts** : 7. Industrialisation et delivery · 8. Sécurité, gouvernance et coûts · 9. Cas pratique de bout en bout
**Exercices participants** : [`exercises/J4_industrialisation_cas_pratique.md`](../exercises/J4_industrialisation_cas_pratique.md)

| Horaire | Durée | Séquence | Format |
| --- | --- | --- | --- |
| 13 h 30 | 30 min | 7.1 Git, revues de code et CI/CD avec Claude Code | Exposé + démo |
| 14 h 00 | 20 min | **Exercice 4.1** — De la branche à la PR relue | Pratique |
| 14 h 20 | 15 min | 7.2 Réutilisabilité et collaboration entre consultants | Exposé |
| 14 h 35 | 35 min | 8. Sécurité, gouvernance, coûts | Exposé + démo |
| 15 h 10 | 15 min | Pause | |
| 15 h 25 | 95 min | **Exercice 4.2 — Cas pratique de bout en bout** (binômes) | Pratique encadrée |
| 17 h 00 | 20 min | Restitutions (3 binômes × 5 min) + débrief | Échange |
| 17 h 20 | 10 min | Quiz, évaluation à chaud, clôture | Individuel |

---

## 13 h 30 — 7.1 Git, revues de code et CI/CD (30 min)

### Claude Code et Git

Claude manipule Git comme un développeur : `git status`, branches, commits, résolution de conflits, et PR via la CLI `gh`.

Règles d'équipe recommandées (déjà en place dans `.claude/settings.json`) :
- `git status`, `git diff`, `git log` autorisés sans confirmation ; **`git commit` et `git push` en `ask`** ;
- une branche par tâche ; jamais de commit direct sur `main` ;
- messages de commit au format de l'équipe (écrit dans `CLAUDE.md`), une ligne de contexte « pourquoi » ;
- **petites PR** : une PR = une intention, relisible en 10 minutes.

Pour travailler en parallèle sans se marcher dessus : les **worktrees Git** (`git worktree add ../retailco-feature-x -b feature-x`), une session Claude Code par worktree.

### Les trois niveaux de revue

| Niveau | Outil | Ce qu'il apporte |
| --- | --- | --- |
| 1. Auto-relecture guidée | `/sql-review fichier.sql`, demande explicite « relis ton diff » | Rapide, mais l'agent relit son propre travail |
| 2. Relecture indépendante | Subagent [`data-reviewer`](../.claude/agents/data-reviewer.md) (contexte vierge, lecture seule, Sonnet), skill intégré `/code-review`, `/security-review` | Regard neuf, sans le biais de la conversation |
| 3. Revue humaine | PR GitHub/GitLab | **Obligatoire** : le consultant signe ce qu'il livre |

Message clé : les niveaux 1 et 2 **préparent** la revue humaine, ils ne la remplacent pas.

### CI/CD : Claude Code dans GitHub Actions

Deux workflows dans le dépôt :
- [`ci.yml`](../.github/workflows/ci.yml) : CI classique (ruff, pytest, génération des données, `dbt build` sur DuckDB). Claude n'y intervient pas : **la CI doit rester déterministe**.
- [`claude.yml`](../.github/workflows/claude.yml) : action officielle `anthropics/claude-code-action@v1`,
  - mode interactif : un commentaire `@claude corrige le test dbt en échec` dans une PR ou une issue déclenche Claude ;
  - mode automatique : à chaque PR, une relecture avec une consigne et une liste blanche d'outils (`--allowedTools`), plafonnée par `--max-turns` et un `timeout-minutes`.

Installation : `/install-github-app` depuis Claude Code (installe l'application GitHub, crée le secret, ouvre la PR du workflow), ou manuellement (application GitHub Claude + secret `ANTHROPIC_API_KEY` ou `CLAUDE_CODE_OAUTH_TOKEN` + copie du workflow).
Sur GitLab : intégration CI/CD équivalente (voir la documentation Claude Code « GitLab CI/CD »).

### Démo (10 min)

1. `git checkout -b fix/fan-out-fct-orders` ; demander à Claude de corriger le fan-out avec un test ;
2. `utilise le subagent data-reviewer pour relire mes changements` → verdict ;
3. « crée la PR avec gh, description en français : contexte, correctif, impact chiffré, tests » ;
4. sur GitHub : la CI tourne, la relecture automatique poste son commentaire ; un `@claude` dans la PR pour une question.

---

## 14 h 00 — Exercice 4.1 : de la branche à la PR relue (20 min)

Chaque participant transforme ses corrections de J3 en **une PR propre** : branche, commits atomiques, relecture `data-reviewer`, description de PR générée puis relue, CI verte.

---

## 14 h 20 — 7.2 Réutilisabilité et collaboration (15 min)

Ce qui se partage, et comment :

| Quoi | Où | Partagé avec |
| --- | --- | --- |
| Instructions projet, permissions, hooks, skills, subagents, règles | `CLAUDE.md`, `.claude/` du dépôt | L'équipe projet (via Git) |
| Préférences personnelles | `~/.claude/`, `CLAUDE.local.md`, `.claude/settings.local.json` | Personne |
| Serveurs MCP du projet | `.mcp.json` (sans secret, variables d'environnement) | L'équipe projet |
| Savoir-faire transverse Keyrus (skill `dbt-model`, revue SQL, audit qualité) | **Plugin** interne publié sur une *marketplace* Git Keyrus | Tous les consultants |
| Règles imposées (interdits, modèles autorisés) | *Managed settings* déployés par l'IT | Toute l'organisation |

Proposition à débattre avec la salle : un **kit de démarrage de mission** Keyrus = un dépôt modèle contenant `CLAUDE.md` type, `.claude/settings.json` sécurisé, hooks, skills Data, et la check-list sécurité ci-dessous. Chaque mission le copie puis l'enrichit des pièges métier du client.

Bonnes pratiques de collaboration :
- `CLAUDE.md` se relit en PR comme du code ; une correction répétée deux fois à Claude → une ligne dans `CLAUDE.md` ;
- documenter les sessions utiles : `/rename` + un résumé dans la PR (prompt, décisions, vérifications) ;
- capitaliser : un skill qui a servi sur 2 missions passe dans le plugin Keyrus.

---

## 14 h 35 — 8. Sécurité, gouvernance et maîtrise des coûts (35 min)

### 8.1 Confidentialité des données clients (15 min)

**Ce qui part chez Anthropic** : Claude Code s'exécute localement, mais tout ce qui entre dans le contexte (prompts, contenu des fichiers lus, sorties de commandes, **y compris des lignes de données** si Claude fait un `select *`) est envoyé au modèle, chiffré en transit (TLS 1.2+).

**Ce qu'Anthropic en fait** (documentation Claude Code, page *Data usage*, novembre 2026) :

| | Comptes commerciaux (Team, Enterprise, API, plateformes cloud) | Comptes grand public (Free, Pro, Max) |
| --- | --- | --- |
| Entraînement des modèles | **Non**, sauf adhésion volontaire (programme partenaire) | Selon le réglage choisi par l'utilisateur |
| Conservation | 30 jours ; **ZDR** (Zero Data Retention, aucune conservation) possible sur Claude for Enterprise après validation d'éligibilité | 30 jours, ou 5 ans si l'utilisateur a accepté l'usage pour l'entraînement |
| En local | Transcriptions en clair dans `~/.claude/projects/` pendant 30 jours (`cleanupPeriodDays`) | Idem |

**Règle Keyrus à poser : uniquement des comptes commerciaux pour du code ou des données client. Jamais un compte personnel.**
Vérifier aussi ce que le contrat du client autorise : certains clients exigent un hébergement dans leur cloud (Bedrock, Google Cloud, Foundry), d'autres interdisent tout outil d'IA générative.

Mesures concrètes en mission :

| Risque | Mesure |
| --- | --- |
| Lecture de secrets | `deny` sur `.env`, profils dbt, `~/.snowflake` ; secrets dans un coffre, jamais dans le dépôt |
| Données personnelles dans le contexte | Travailler sur des échantillons anonymisés ou synthétiques ; consigne « agrégats uniquement, 20 lignes max » ; rôle Snowflake sans accès aux colonnes sensibles (masquage dynamique) |
| Action destructrice | Rôle en lecture seule pour l'exploration ; hooks de blocage ; jamais d'identifiants de production sur le poste |
| Injection de prompt (instructions malveillantes cachées dans un fichier, une page web, une donnée) | Mode `default` sur du contenu non maîtrisé ; ne pas « piper » de contenu non fiable ; `curl`/`wget` en `deny` ; bac à sable (`/sandbox`) pour isoler le système de fichiers et le réseau |
| Fuite par la télémétrie / le feedback | Comptes commerciaux ; variable `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` si le client l'exige ; ne pas utiliser `/feedback` sur du code client |
| Copie locale des sessions | Réduire `cleanupPeriodDays` ; chiffrement du disque du poste |

### 8.2 Contrôle humain et risques liés à l'IA (10 min)

Risques à nommer explicitement :
- **le code plausible mais faux** (les 4 bugs de J3 auraient pu être écrits par une IA) ;
- **l'excès de confiance** : plus l'outil est bon, moins on relit ;
- **la dérive de périmètre** : l'agent « améliore » des fichiers qu'on ne lui a pas demandé de toucher ;
- **le contournement des tests** : modifier le test plutôt que le code ;
- **la dépendance** : un consultant qui ne comprend plus le code qu'il livre.

Garde-fous : Plan Mode avant toute tâche non triviale, mode `default` ou `acceptEdits` (pas `bypassPermissions` hors conteneur), tests écrits ou validés par l'humain, revue indépendante, **PR relue et signée par un humain**, traçabilité (description de PR qui mentionne l'usage de Claude et les vérifications faites).

Pour l'entreprise : *managed settings* (interdits imposés, désactivation possible de `bypassPermissions` et du mode `auto`), `CLAUDE.md` d'entreprise, suivi d'usage par OpenTelemetry, hooks `ConfigChange` pour auditer les modifications de configuration.

### 8.3 Optimiser les consommations (10 min)

Repères (documentation Claude Code, page *Manage costs*) : environ 13 $ par développeur et par jour actif, 150–250 $ par mois, moins de 30 $ par jour actif pour 90 % des utilisateurs.

Le coût est proportionnel **au volume de contexte traité** : chaque échange renvoie toute la conversation.

| Levier | Geste |
| --- | --- |
| Contexte | `/clear` entre deux tâches ; `/compact` avec consigne ; `CLAUDE.md` < 200 lignes ; procédures longues en skills (chargées à la demande) |
| Modèle | Sonnet par défaut ; Opus pour l'architecture et les raisonnements difficiles ; Haiku pour les subagents simples (`model: haiku`) ; `/effort` plus bas sur les tâches simples |
| Prompts | Spécifiques (« dans `auth.ts`… ») plutôt que « améliore le dépôt » qui déclenche une lecture massive |
| Outils | CLI (`gh`, `dbt`, `snow`) plutôt que MCP quand c'est équivalent ; désactiver les serveurs MCP inutilisés (`/mcp`) ; hooks qui filtrent les sorties verbeuses (ne renvoyer que les tests en échec) |
| Délégation | Subagents pour les sorties volumineuses (logs, tests) : seul le résumé revient |
| Méthode | Plan Mode pour éviter de coder dans la mauvaise direction ; `Échap` tôt ; tester par petits incréments |
| Suivi | `/usage` (session, répartition par skill/subagent/MCP, recommandations), `/context`, `/insights` ; côté organisation : limites de dépense, tableaux de bord d'administration |

Côté Snowflake, ne pas oublier **le coût de calcul déclenché par l'agent** : entrepôt XS dédié, `AUTO_SUSPEND = 60`, moniteur de ressources (voir [`snowflake/setup_training_env.sql`](../snowflake/setup_training_env.sql)).

### Démo (5 min)

`/usage` puis `/context` en fin de session de démo : lire avec la salle la répartition (fichiers lus, outils MCP, `CLAUDE.md`) et les recommandations.

---

## 15 h 25 — Exercice 4.2 : cas pratique de bout en bout (95 min, binômes)

### Le besoin (à lire à voix haute)

> La direction commerciale de RetailCo veut **identifier chaque mois les clients à risque de départ** pour déclencher une campagne de rétention.
> Un client est « à risque » s'il n'a passé aucune commande non annulée depuis **plus de 90 jours** (**60 jours** pour les VIP), alors qu'il a passé **au moins 2 commandes** dans les 12 mois précédents.
> Livrables : une table dbt exploitable par l'équipe BI, et un export CSV quotidien pour l'outil CRM (Customer Relationship Management) **sans donnée personnelle en clair**.

### Étapes imposées et jalons

| Jalon | Temps indicatif | Attendu | Thème |
| --- | --- | --- | --- |
| 1. Cadrage | 10 min | Questions au « métier » (le formateur), hypothèses écrites dans `docs/cas_pratique.md` : date de référence, statuts retenus, grain | 2 |
| 2. Exploration et plan | 15 min | Plan Mode : modèles existants réutilisés, nouveaux fichiers, tests prévus. Plan validé par le formateur | 2, 3 |
| 3. Modèle dbt | 25 min | `marts/mart_customers_at_risk.sql` + YAML documenté et testé, `dbt build` vert | 4, 5 |
| 4. Export Python | 20 min | `src/retail_pipeline/export_at_risk.py` + tests pytest ; email pseudonymisé (hachage) | 4, 5, 8 |
| 5. Livraison | 15 min | Branche, relecture `data-reviewer`, PR avec description, CI verte | 7 |
| 6. Bilan coûts | 5 min | Relevé `/usage` de la session, une amélioration de `CLAUDE.md` ou un skill proposé | 6, 8 |

### Réponses du « métier » (à donner seulement si on les demande — c'est l'objet du jalon 1)

- Date de référence : paramètre `as_of_date`, par défaut **2026-09-01** (les données s'arrêtent fin août 2026) ;
- commandes prises en compte : statuts `delivered`, `shipped`, `returned` (pas `cancelled`) ; les dates futures sont ignorées ;
- « 12 mois précédents » = les 365 jours avant `as_of_date` ;
- grain : une ligne par client, **tous** les clients (avec un booléen `is_at_risk`) ;
- export : uniquement les clients à risque, colonnes `customer_key` (SHA-256 de l'email normalisé), `segment`, `days_since_last_order`, `orders_last_12m`, `revenue_last_12m` ; aucun nom, aucun email en clair.

### Grille d'évaluation

Voir [annexes/evaluation.md](annexes/evaluation.md). Corrigé : [`solutions/dbt_project/models/marts/mart_customers_at_risk.sql`](../solutions/dbt_project/models/marts/mart_customers_at_risk.sql) et [`solutions/src/retail_pipeline/export_at_risk.py`](../solutions/src/retail_pipeline/export_at_risk.py).

### Notes formateur

- Résultat de référence (corrigé, `as_of_date = 2026-09-01`) : **665 clients à risque** sur 2 000 (291 VIP, 202 B2B, 172 B2C) ;
  **641 exportés**, 24 étant exclus faute d'email. Un écart de quelques dizaines vient généralement d'une hypothèse différente (statuts, borne des 365 jours).
- Passer dans les binômes au jalon 2 : **refuser un plan sans tests ni grain explicite**.
- Pièges fréquents : oublier le seuil VIP ; compter les commandes annulées ; utiliser `current_date` (résultat non reproductible) ; joindre `fct_orders` non corrigé (fan-out) ; exporter l'email en clair « pour tester » ; hachage sans normalisation (casse, espaces) ; dates futures qui donnent un `days_since_last_order` négatif.
- Si un binôme termine tôt : rendre le modèle incrémental, ou ajouter une GitHub Action planifiée qui produit l'export.

---

## 17 h 00 — Restitutions (20 min)

Trois binômes, 5 minutes chacun : le plan initial, ce que Claude a bien fait, ce qu'il a fallu corriger, le coût de la session.
Débrief : comparer les définitions retenues (les écarts de chiffres viennent presque toujours d'hypothèses différentes, pas de bugs).

## 17 h 20 — Clôture (10 min)

- Quiz de 10 questions ([annexes/evaluation.md](annexes/evaluation.md)) ;
- évaluation à chaud ;
- remettre l'[aide-mémoire](annexes/aide-memoire.md) et l'accès au dépôt (branche `solutions` ouverte à tous).
