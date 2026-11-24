# Claude Code Training for Data Consultants — Keyrus

A **4 half-day** training (a half-day is either a morning or an afternoon) on using Claude Code for Data projects (SQL, Python, dbt, Snowflake).

| You are… | Start with |
| --- | --- |
| **Trainer** | [`docs/README.md`](docs/README.md): objectives, schedule, timed guide for each half-day, preparation, assessment |
| **Participant** | The "Installation" section below, then the exercise sheets in [`exercises/`](exercises) |

## Training breakdown: 4 half-days, 9 themes

Each half-day lasts **4 hours**. The start time is up to the organiser (for example 09:00 or 13:30).

| Half-day | Themes | Content | Timed guide | Slides |
| --- | --- | --- | --- | --- |
| **1** | **1 – 2** | 1. Claude Code fundamentals<br>2. Prompting & context engineering | [Half-day 1](docs/01-half-day-1.md) | [1-fundamentals-prompting-context.pptx](slides/1-fundamentals-prompting-context.pptx) |
| **2** | **3 – 4** | 3. Code exploration<br>4. AI-assisted Data development | [Half-day 2](docs/02-half-day-2.md) | [2-code-exploration-data-development.pptx](slides/2-code-exploration-data-development.pptx) |
| **3** | **5 – 6** | 5. Testing, debugging & quality<br>6. Integrations (MCP, Skills, hooks) and automation | [Half-day 3](docs/03-half-day-3.md) | [3-testing-quality-integrations.pptx](slides/3-testing-quality-integrations.pptx) |
| **4** | **7 – 8, then 9** | 7. Delivery (Git, CI/CD, reviews)<br>8. Security, governance, costs<br>9. **End-to-end case study** (closing) | [Half-day 4](docs/04-half-day-4.md) | [4-delivery-security-costs-case-study.pptx](slides/4-delivery-security-costs-case-study.pptx) |

### What the trainer guide contains ([`docs/`](docs/README.md))

- **A minute-by-minute plan** for each half-day (4 hours): key messages, demo scripts, trainer notes. Times are given as elapsed time from the start of the session.
- [Preparation checklist](docs/00-preparation.md)
- A one-page [cheat sheet](docs/annexes/cheat-sheet.md)
- A 10-question quiz and the [case study grading grid](docs/annexes/evaluation.md)
- [Trainer FAQ](docs/annexes/trainer-faq.md)

---

## RetailCo — the running project

A small, realistic data project (Python + DuckDB/Snowflake + dbt) used throughout the 4 half-days.
It **deliberately** contains technical debt and bugs: it is the playground for the exercises.

## Installation (15 min, to do before the first session)

```bash
# 1. Claude Code (macOS / Linux / WSL) — Windows: irm https://claude.ai/install.ps1 | iex
curl -fsSL https://claude.ai/install.sh | bash
claude --version

# 2. Project
git clone https://github.com/keyrus-formation/keyrus-claude-code-training && cd keyrus-claude-code-training
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"            # + ".[snowflake]" if you use the Snowflake environment
cp .env.example .env

# 3. Data + local warehouse
python scripts/generate_data.py
python -m retail_pipeline.pipeline
cd dbt_project && DBT_PROFILES_DIR=. dbt build ; cd ..
```

`dbt build` must finish with **1 failing test** (`unique_fct_orders_order_id`): this is expected,
it is the subject of an exercise. Useful tools: `jq` (used by the hooks), `uv` (dbt MCP server), `gh`.

## Structure

| Path | Content |
| --- | --- |
| `data/raw/` | Generated source CSVs (customers, orders, lines, payments, products) — write-protected |
| `src/retail_pipeline/` | Python pipeline: extract → transform → quality → load |
| `src/retail_pipeline/legacy_report.py` | Slow legacy report (optimisation exercise) |
| `sql/legacy/` | Legacy Snowflake query to migrate to dbt |
| `dbt_project/` | Staging and marts models, DuckDB (`dev`) and Snowflake (`snowflake`) targets |
| `tests/` | pytest tests (green… but incomplete) |
| `.claude/` | Team-shared permissions, hooks, skills, subagent and rules |
| `.mcp.json.example` | dbt and Snowflake MCP servers (copy to `.mcp.json`) |
| `.github/workflows/` | CI (lint, tests, dbt) and Claude Code GitHub Actions integration |
| `exercises/` | Exercise sheets, per half-day |
| `solutions/` | Solutions (hand out only at the end of the session) |
| `docs/` | Trainer guide, cheat sheet, quiz, FAQ |
| `slides/` | PowerPoint decks (one per half-day) and the scripts that generate them |
| `snowflake/` | Script that creates the training Snowflake environment |

## Reference commands

```bash
pytest -q                                              # unit tests
ruff check src tests                                   # lint
python -m retail_pipeline.pipeline                     # load data/raw into DuckDB
cd dbt_project && DBT_PROFILES_DIR=. dbt build         # dbt models + tests (DuckDB)
DBT_TARGET=snowflake dbt build                          # same on Snowflake
```
