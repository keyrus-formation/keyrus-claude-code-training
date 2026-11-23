# Guide du formateur — Claude Code pour les consultants Data (Keyrus)

> Formation de **4 après-midi (4 × 3 h 45 de face-à-face, 15 h au total)** pour des consultants Data
> de niveaux hétérogènes : certains n'ont jamais utilisé d'agent IA, d'autres connaissent déjà
> GitHub Copilot, Cursor ou Claude Code. Le fil rouge est le projet **RetailCo** de ce dépôt
> (Python, SQL, dbt, DuckDB en local, Snowflake en option).

## Objectifs pédagogiques

À l'issue de la formation, chaque participant sait :

1. expliquer ce qu'est un agent IA (intelligence artificielle) et en quoi il diffère d'un LLM (Large Language Model, grand modèle de langage) utilisé en mode conversationnel ;
2. installer, configurer et piloter Claude Code (modes de permission, Plan Mode, gestion du contexte) ;
3. rédiger des instructions efficaces et maintenir un `CLAUDE.md` de projet utile ;
4. explorer et documenter un dépôt Data inconnu (architecture, lignage, dépendances) en moins d'une heure ;
5. produire avec Claude Code du code SQL, Python et dbt testé, portable DuckDB / Snowflake ;
6. détecter et corriger des bugs de données (fan-out, dédoublonnage, formats) avec une démarche « test d'abord » ;
7. étendre Claude Code avec des MCP (Model Context Protocol), des Skills, des hooks et des subagents ;
8. intégrer Claude Code dans un flux Git / CI/CD (intégration continue / déploiement continu) avec revue humaine ;
9. appliquer les règles de confidentialité des données clients, de gouvernance et de maîtrise des coûts.

## Déroulé

| Après-midi | Thèmes | Fil rouge | Fichier |
| --- | --- | --- | --- |
| **J1** — Prendre en main | 1. Fondamentaux · 2. Prompting & context engineering | Installation, premier contact avec RetailCo, `/init`, rédaction du `CLAUDE.md`, Plan Mode | [01-apres-midi-1.md](01-apres-midi-1.md) |
| **J2** — Comprendre et produire | 3. Exploration de code · 4. Développement Data assisté | Cartographie du dépôt, migration d'une requête Snowflake en dbt, optimisation d'un script pandas (90 s → 0,2 s) | [02-apres-midi-2.md](02-apres-midi-2.md) |
| **J3** — Fiabiliser et outiller | 5. Testing, debugging & qualité · 6. Intégrations & automatisation | Chasse aux 4 bugs cachés (≈ 570 k€ de CA perdu), tests de qualité, MCP dbt, Skills, hooks | [03-apres-midi-3.md](03-apres-midi-3.md) |
| **J4** — Industrialiser | 7. Delivery · 8. Sécurité, gouvernance, coûts · 9. Cas pratique de bout en bout | PR (pull request) relue par un subagent et par la CI, cas pratique « clients à risque » en binôme | [04-apres-midi-4.md](04-apres-midi-4.md) |

Le thème 9 (mise en pratique) n'est pas concentré sur J4 : **chaque après-midi consacre environ 50 % du temps à des exercices** sur RetailCo ;
J4 se termine par le cas pratique de bout en bout.

Horaires types d'un après-midi : 13 h 30 – 17 h 30, avec une pause de 15 min vers 15 h 30.

## Contenu du dossier `docs/`

| Fichier | Usage |
| --- | --- |
| [00-preparation.md](00-preparation.md) | Check-list J-7 / J-1 / Jour J, comptes, environnement Snowflake, budget |
| [01 … 04-apres-midi-N.md](01-apres-midi-1.md) | Déroulé minuté, messages clés, démos pas à pas, notes formateur |
| [annexes/aide-memoire.md](annexes/aide-memoire.md) | Aide-mémoire d'une page à distribuer aux participants |
| [annexes/evaluation.md](annexes/evaluation.md) | Quiz de fin de formation (corrigé) et grille d'évaluation du cas pratique |
| [annexes/faq-formateur.md](annexes/faq-formateur.md) | Questions fréquentes et réponses, incidents courants |

Les énoncés destinés aux participants sont dans [`../exercises/`](../exercises), les corrigés dans [`../solutions/`](../solutions).

## Hypothèses retenues

- **Langue** : français pour tout le support ; les mots-clés techniques (prompt, hook, skill…) restent en anglais.
- **Public** : niveaux mixtes. Les blocs « 🚀 Pour aller plus loin » occupent les plus rapides sans ralentir le groupe.
- **Environnement** : chaque participant a un poste avec terminal, Python 3.10+, Git et un compte Claude
  (Team/Enterprise Keyrus ou clé API — Application Programming Interface — de la Claude Console).
  DuckDB remplace Snowflake si l'accès Snowflake n'est pas disponible : tous les exercices fonctionnent sans Snowflake.
- **Versions** : contenu vérifié sur la documentation Claude Code de novembre 2026. Claude Code évolue vite :
  relancer `claude --version` et parcourir le changelog la veille de la session (voir [00-preparation.md](00-preparation.md)).

## Messages clés de la formation (à répéter)

1. **Un agent agit, il ne se contente pas de répondre** : il lit, exécute, modifie. D'où l'importance des permissions et de la revue.
2. **Le contexte est la ressource rare** : ce qui entre dans la fenêtre de contexte détermine la qualité *et* le coût.
3. **Explorer → planifier → coder → vérifier** : le Plan Mode et les tests sont les deux garde-fous les plus rentables.
4. **Donner à Claude un moyen de vérifier son travail** (tests, `dbt build`, résultat attendu) vaut mieux que de longues explications.
5. **Le consultant reste responsable** de chaque ligne livrée chez le client, qu'elle ait été écrite par lui ou par Claude.
