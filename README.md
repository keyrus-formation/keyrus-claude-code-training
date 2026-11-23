# Formation Claude Code pour les consultants Data — Keyrus

Formation de **4 après-midi** pour apprendre à utiliser Claude Code sur des projets Data (SQL, Python, dbt, Snowflake).

| Vous êtes… | Commencez par |
| --- | --- |
| **Formateur** | [`docs/README.md`](docs/README.md) : objectifs, déroulé, guide minuté de chaque après-midi, préparation, évaluation |
| **Participant** | La section « Installation » ci-dessous, puis les énoncés dans [`exercises/`](exercises) |

## Découpage de la formation : 4 après-midi, 9 thèmes

Chaque après-midi dure **4 h, de 13h30 à 17h30**.

| Après-midi | Thèmes | Contenu | Guide minuté |
| --- | --- | --- | --- |
| **Jour 1** | **1 – 2** | 1. Fondamentaux de Claude Code<br>2. Prompting & context engineering | [J1](docs/01-apres-midi-1.md) |
| **Jour 2** | **3 – 4** | 3. Exploration de code<br>4. Développement Data assisté par IA | [J2](docs/02-apres-midi-2.md) |
| **Jour 3** | **5 – 6** | 5. Testing, debugging & qualité<br>6. Intégrations (MCP, Skills, hooks) et automatisation | [J3](docs/03-apres-midi-3.md) |
| **Jour 4** | **7 – 8, puis 9** | 7. Delivery (Git, CI/CD, revues)<br>8. Sécurité, gouvernance, coûts<br>9. **Cas pratique de bout en bout** (clôture) | [J4](docs/04-apres-midi-4.md) |

### Ce que contient le guide du formateur ([`docs/`](docs/README.md))

- **Un plan minute par minute** pour chaque après-midi (13h30 – 17h30) : messages clés, scripts de démo, notes du formateur.
- [Checklist de préparation](docs/00-preparation.md)
- [Aide-mémoire](docs/annexes/aide-memoire.md) d'une page
- Quiz de 10 questions et [grille de notation du cas pratique](docs/annexes/evaluation.md)
- [FAQ formateur](docs/annexes/faq-formateur.md)

---

## RetailCo — le projet fil rouge

Petit projet data réaliste (Python + DuckDB/Snowflake + dbt) utilisé pendant les 4 après-midi.
Il contient **volontairement** de la dette technique et des bugs : c'est le terrain de jeu des exercices.

## Installation (15 min, à faire avant la première session)

```bash
# 1. Claude Code (macOS / Linux / WSL) — Windows : irm https://claude.ai/install.ps1 | iex
curl -fsSL https://claude.ai/install.sh | bash
claude --version

# 2. Projet
git clone <url-du-repo> retailco && cd retailco
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"            # + ".[snowflake]" si vous utilisez l'environnement Snowflake
cp .env.example .env

# 3. Données + entrepôt local
python scripts/generate_data.py
python -m retail_pipeline.pipeline
cd dbt_project && DBT_PROFILES_DIR=. dbt build ; cd ..
```

Le `dbt build` doit se terminer avec **1 test en échec** (`unique_fct_orders_order_id`) : c'est normal,
c'est l'objet d'un exercice. Outils utiles : `jq` (utilisé par les hooks), `uv` (serveur MCP dbt), `gh`.

## Structure

| Chemin | Contenu |
| --- | --- |
| `data/raw/` | CSV sources générés (clients, commandes, lignes, paiements, produits) — protégés en écriture |
| `src/retail_pipeline/` | Pipeline Python extract → transform → quality → load |
| `src/retail_pipeline/legacy_report.py` | Rapport historique lent (exercice d'optimisation) |
| `sql/legacy/` | Requête Snowflake historique à migrer en dbt |
| `dbt_project/` | Modèles staging et marts, cibles DuckDB (`dev`) et Snowflake (`snowflake`) |
| `tests/` | Tests pytest (verts… mais incomplets) |
| `.claude/` | Permissions, hooks, skills, subagent et règles partagés de l'équipe |
| `.mcp.json.example` | Serveurs MCP dbt et Snowflake (à copier en `.mcp.json`) |
| `.github/workflows/` | CI (lint, tests, dbt) et intégration Claude Code GitHub Actions |
| `exercises/` | Énoncés des exercices, par après-midi |
| `solutions/` | Corrigés (à ne distribuer qu'en fin de session) |
| `docs/` | Guide du formateur, aide-mémoire, quiz, FAQ |
| `snowflake/` | Script de création de l'environnement Snowflake de formation |

## Commandes de référence

```bash
pytest -q                                              # tests unitaires
ruff check src tests                                   # lint
python -m retail_pipeline.pipeline                     # charge data/raw dans DuckDB
cd dbt_project && DBT_PROFILES_DIR=. dbt build         # modèles + tests dbt (DuckDB)
DBT_TARGET=snowflake dbt build                          # même chose sur Snowflake
```
