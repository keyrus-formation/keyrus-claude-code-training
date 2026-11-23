# Préparation du formateur

## J-7 : comptes et accès

- [ ] **Comptes Claude** pour chaque participant. **Aucune clé API (Application Programming Interface) n'est à distribuer** :
  chacun se connecte avec son compte au premier lancement de `claude`. Options, par ordre de préférence :
  1. **sièges Claude Team / Enterprise** de l'organisation Keyrus : connexion par navigateur, consommation prise
     sur le quota du siège, limites de dépense réglables dans l'administration ;
  2. **membres d'une organisation Claude Console** (facturation à l'usage) : connexion par navigateur
     avec le compte Console ; un workspace « Claude Code » est créé automatiquement, avec suivi par utilisateur
     et limite de dépense (voir « Budget ») ;
  3. **fournisseur cloud** (Amazon Bedrock, Google Cloud, Microsoft Foundry) si les flux doivent rester dans un compte cloud.
  À éviter : une clé API unique partagée via `ANTHROPIC_API_KEY` (pas de suivi individuel, clé dispersée sur tous les postes).
  Seule exception : la démo GitHub Actions de J4 utilise **un** secret de dépôt (`ANTHROPIC_API_KEY` ou
  `CLAUDE_CODE_OAUTH_TOKEN` généré par `claude setup-token`), détenu par le formateur.
- [ ] **Débit (rate limits)** : une session de formation = tout le monde en même temps. La documentation Claude Code
  recommande de prévoir plus de TPM (tokens par minute) par utilisateur en cas de forte concurrence, comme une formation en direct.
  Pour 12 participants sur la Console, viser au moins 100 k–150 k TPM par utilisateur.
- [ ] **Dépôt** : créer le dépôt GitHub de la session à partir de celui-ci (bouton *Use this template* ou fork),
  **sans le dossier `solutions/`**, et y ajouter les participants. Garder `solutions/` dans une branche privée `formateur`.
- [ ] **Snowflake (optionnel)** : exécuter [`../snowflake/setup_training_env.sql`](../snowflake/setup_training_env.sql) avec un rôle
  `ACCOUNTADMIN` (ou `SYSADMIN` + `SECURITYADMIN`). Il crée la base `RETAILCO`, un entrepôt XS avec auto-suspend à 60 s,
  un moniteur de ressources plafonné, un rôle `TRAINING_ROLE` et un schéma de travail par participant.
- [ ] Envoyer aux participants le **mail de pré-requis** (ci-dessous) avec le README du dépôt.

### Mail de pré-requis (à adapter)

> Bonjour à tous,
> Pour la formation Claude Code des [dates], merci de préparer votre poste **avant la première session** (15 min) :
> 1. Installer Claude Code : `curl -fsSL https://claude.ai/install.sh | bash` (macOS/Linux/WSL)
>    ou `irm https://claude.ai/install.ps1 | iex` (Windows PowerShell), puis vérifier avec `claude --version`.
> 2. Vérifier Python 3.10+, Git, et installer `jq` et `uv`.
> 3. Cloner le dépôt [URL] et suivre la section « Installation » du README jusqu'au `dbt build`.
> 4. Lancer `claude` dans le dossier et vous connecter avec [compte Keyrus / clé fournie].
> En cas de blocage, écrivez-moi : on règle les problèmes d'installation avant le jour J, pas pendant.

## J-1 : vérifications

- [ ] `claude --version` et lecture du changelog : une commande ou un raccourci a-t-il changé ? Ajuster les slides/démos.
- [ ] Cloner le dépôt sur une machine vierge et dérouler le README de bout en bout (≈ 10 min).
  Résultat attendu : `pytest` vert (4 tests), `dbt build` avec **exactement 1 échec** (`unique_fct_orders_order_id`).
- [ ] Tester les hooks : demander à Claude de modifier `.env` → doit être bloqué.
- [ ] Préparer un terminal de démo lisible : police ≥ 18 pt, thème clair, `/statusline` affichant le contexte.
- [ ] Préparer une **branche de secours par après-midi** (`etat-J2`, `etat-J3`, `etat-J4`) contenant l'état attendu
  en début de session, pour qu'un participant en retard reparte d'une base saine.
- [ ] Imprimer l'[aide-mémoire](annexes/aide-memoire.md) (1 par participant).

## Jour J : avant d'ouvrir la salle

- [ ] Wi-Fi testé, accès à `claude.ai` et `api.anthropic.com` non filtré par le proxy client.
- [ ] Vidéoprojecteur : démo en **mode `default`** (permissions demandées) pour que la salle voie chaque action.
- [ ] Ouvrir la Claude Console / la page d'administration pour suivre la consommation en direct.

## Budget et consommation

Ordres de grandeur officiels (documentation Claude Code, page *Manage costs*) : en entreprise, le coût moyen est
d'environ **13 $ par développeur et par jour actif**, **150–250 $ par mois**, et reste sous **30 $ par jour actif pour 90 % des utilisateurs**.
Une formation est plus intensive qu'une journée normale (tout le monde explore en même temps, prompts larges) :
prévoir **15–30 $ par participant et par après-midi** sur une facturation à l'usage, soit 60–120 $ par participant
pour les 4 sessions, et fixer la limite de dépense du workspace en conséquence.

Leviers si la consommation dérape : imposer Sonnet comme modèle par défaut (`/model`), rappeler `/clear` entre exercices,
interdire les prompts du type « améliore tout le dépôt ».

## Matériel pédagogique

| Élément | Où |
| --- | --- |
| Projet fil rouge | racine du dépôt (voir README) |
| Énoncés participants | `exercises/J1…J4` |
| Corrigés | `solutions/` (à retirer de la copie participants) |
| Script Snowflake | `snowflake/setup_training_env.sql` |
| Configuration Claude Code partagée | `.claude/` (permissions, hooks, skills, subagent, règles) |

## Constitution des binômes

Pour les exercices en binôme (J2, J4), associer un profil « déjà utilisateur d'IA » à un profil « débutant »,
et un profil plutôt SQL/dbt à un profil plutôt Python quand c'est possible.
