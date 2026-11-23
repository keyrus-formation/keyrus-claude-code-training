# FAQ formateur et incidents courants

## Questions fréquentes des participants

**« Est-ce que Claude garde mon code pour s'entraîner ? »**
Pas avec un compte commercial (Team, Enterprise, API, plateformes cloud) : Anthropic n'entraîne pas ses modèles sur ces données, sauf adhésion volontaire de l'organisation. Conservation standard de 30 jours, ZDR (Zero Data Retention) possible sur Enterprise. Les comptes grand public (Free, Pro, Max) dépendent du réglage de l'utilisateur. Voir J4, section 8.1.

**« Faut-il une clé API par participant ? »**
Non. Chacun se connecte avec son compte (siège Team/Enterprise, ou membre d'une organisation Claude Console). Seule la démo GitHub Actions utilise un secret de dépôt. Voir [00-preparation.md](../00-preparation.md).

**« Quelle différence avec GitHub Copilot ou Cursor ? »**
Rester factuel et éviter le dénigrement : Claude Code est centré sur le terminal et l'agent (boucle autonome, outils shell, hooks, subagents, MCP, mode non interactif pour la CI). Il s'utilise aussi dans VS Code et JetBrains. Le choix dépend souvent de ce que le client autorise.

**« Peut-on l'utiliser chez un client qui interdit l'envoi de code à l'extérieur ? »**
Pas sans accord écrit du client. Options à discuter avec lui : hébergement dans son propre cloud (Amazon Bedrock, Google Cloud, Microsoft Foundry), ZDR, travail sur données synthétiques. En cas de doute : non.

**« Claude peut-il se connecter directement à notre Snowflake ? »**
Oui, par la CLI `snow` ou par un serveur MCP (dont le serveur MCP géré par Snowflake), **avec un rôle en lecture seule** et sans données de production identifiantes. Voir J3, section 6.2.

**« Comment éviter de valider 50 demandes de permission ? »**
Pré-autoriser les commandes sûres et fréquentes dans `.claude/settings.json` (`allow`), utiliser `acceptEdits` sur du code qu'on relit, le bac à sable (`/sandbox`), ou le mode `auto` si l'organisation l'autorise. Jamais `bypassPermissions` hors conteneur.

## Incidents courants

| Symptôme | Cause probable | Solution |
| --- | --- | --- |
| `claude: command not found` après installation | Dossier d'installation absent du PATH | Ouvrir un nouveau terminal ; voir la page *Troubleshoot installation* de la documentation |
| `The token '&&' is not a valid statement separator` | Commande CMD lancée dans PowerShell | Utiliser `irm https://claude.ai/install.ps1 \| iex` |
| Les hooks ne se déclenchent pas | Script non exécutable ou `jq` absent | `chmod +x .claude/hooks/*.sh`, installer `jq`, vérifier avec `/hooks` |
| Les hooks échouent sous Windows natif | Scripts Bash | Utiliser WSL ou Git for Windows |
| `dbt build` : « Could not find profile » | `DBT_PROFILES_DIR` non défini | Lancer depuis `dbt_project/` avec `DBT_PROFILES_DIR=.` |
| DuckDB : « Could not set lock on file » | Deux processus ouvrent `retail.duckdb` (ex. un notebook + dbt) | Fermer l'autre connexion |
| Serveur MCP dbt « failed » | `uvx` introuvable dans le PATH de Claude Code | Donner le chemin complet de `uvx` (`which uvx`) |
| Message de limite d'usage en pleine session | Quota du siège ou limite de débit de l'organisation | Passer à Sonnet, `/clear`, prévoir un débit plus élevé pour les sessions collectives |
| Claude « tourne en rond » | Contexte pollué, objectif flou | `Échap`, `/clear`, reformuler avec un critère de vérification |
| Un participant a « tout cassé » | — | `git stash` ou `git checkout etat-JN` (branches de secours) |
