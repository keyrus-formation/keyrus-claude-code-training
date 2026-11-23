# Half-day 2 — Understanding an existing codebase and producing Data code

**Themes covered**: 3. Code understanding and exploration · 4. AI-assisted Data development
**Participant exercises**: [`exercises/HD2_exploration_development.md`](../exercises/HD2_exploration_development.md)

> The session start time is up to the organiser (e.g. 09:00 or 13:30). All timings below are offsets from the start of the session (0:00 to 4:00).

| Offset | Duration | Sequence | Format |
| --- | --- | --- | --- |
| 0:00 | 10 min | Back to HD1: a `CLAUDE.md` shown on screen | Discussion |
| 0:10 | 25 min | 3.1 Explore an unfamiliar repository | Talk + demo |
| 0:35 | 35 min | **Exercise 2.1** — Map RetailCo | Individual practice |
| 1:10 | 15 min | 3.2 Document the existing code | Demo |
| 1:25 | 30 min | 4.1 Generate and modify SQL / Python / dbt | Talk + demo |
| 1:55 | 15 min | Break | |
| 2:10 | 50 min | **Exercise 2.2** — Migrate a Snowflake query to a dbt model | Pairs |
| 3:00 | 15 min | 4.2 Optimise existing code | Demo |
| 3:15 | 35 min | **Exercise 2.3** — Optimise the legacy report | Individual |
| 3:50 | 10 min | Wrap-up and HD3 preparation | Discussion |

---

## 0:00 — Back to HD1 (10 min)

Display a volunteer's `CLAUDE.md` and compare it with the model solution. Question to the room: "which business pitfalls did `/init` miss?"
Expected answer: the amount format, multiple versions of orders, split payments. They will come back later.

---

## 0:10 — 3.1 Explore an unfamiliar repository (25 min)

### Key messages

Typical consultant situation: you arrive on an engagement, facing a repository with 300 dbt models and 40 Python scripts, no up-to-date documentation, and 2 days to become operational.
Claude Code is particularly strong here: it reads fast, cross-references files and answers precise questions.

Funnel approach:

1. **Overview**: "explain the architecture of this repository: layers, data flows, technologies, entry points".
2. **Data flow**: "trace the path of an order from the raw CSV to `fct_orders`, file by file".
3. **Dependencies**: "which Python dependencies are actually imported? which are declared but unused?", "which dbt models depend on `stg_orders`?".
4. **Targeted questions**: "where are currencies handled?", "what happens if an amount is empty?".
5. **Risk areas**: "which parts of the code look fragile or inconsistent to you? cite the lines".

Good practices:
- stay in Plan Mode or `default` mode: we explore, we do not modify anything;
- **ask for files and line numbers to be cited**, and check 1 or 2 claims yourself: Claude can be wrong on a detail;
- for a large repository, ask for an exploration subagent ("use subagents to explore the staging and marts folders in parallel"): the detail of the reads stays out of the main conversation, only the summary comes back;
- rely on native tools: `dbt ls --select +fct_orders`, `dbt docs generate` (`manifest.json` contains the full lineage), `git log --stat` to see what changes.

### Demo (10 min)

```text
explain the lineage of fct_orders to me: sources, intermediate models, tests. Use dbt ls
and the SQL files, and cite the files.
```

Then:

```text
git log contains only one commit, so there is no history: from reading the code alone, what are the 3 riskiest
areas of the project? do not modify anything.
```

Depending on the run, Claude often spots the join on payments or the deduplication. **Do not validate or correct anything now**: "we note it, and come back to it in HD3".

---

## 0:35 — Exercise 2.1: map RetailCo (35 min)

Deliverable: a `docs/ARCHITECTURE.md` file generated with Claude, containing a Mermaid diagram of the flow, the list of models and their grains, the dependencies, and an "open questions" section.
Success criterion: a newcomer understands the project after 5 minutes of reading, and **every claim has been verified** (ticked in the document).

---

## 1:10 — 3.2 Document the existing code (15 min)

Three levels of documentation, from most to least durable:

| Level | Example | Typical prompt |
| --- | --- | --- |
| In the code | Docstrings, comments on business rules | "add docstrings to the public functions of `transform.py`, without changing the code" |
| In dbt | Model and column `description` in the YAML files | "complete the descriptions in `_staging.yml` from the SQL; flag what you cannot infer" |
| In the repository | `ARCHITECTURE.md`, `README` | (exercise 2.1) |

Key message: **generated documentation describes what the code does, not what it should do**. If the code is wrong (as it is here), the documentation will faithfully describe the bug.
Always ask for an "assumptions and points to validate with the business" section.

---

## 1:25 — 4.1 Generate and modify SQL, Python and dbt (30 min)

### Key messages

- **Give the dialect and the target**: "Snowflake SQL", "compatible with DuckDB and Snowflake via the project macros".
- **Give the grain** before any query: "one row per customer and per month".
- **Give the real names**: let Claude read the existing models rather than describing columns from memory.
- **Require verification**: "compile with `dbt compile`, then `dbt build --select model+` and fix until everything passes".
- **Small steps**: staging first, then mart; one model at a time.

Snowflake specifics to remind people of (and to put in `CLAUDE.md` at the client):

| Topic | What to specify in the prompt |
| --- | --- |
| Deduplication | `QUALIFY ROW_NUMBER() OVER (...) = 1` (DuckDB supports it too) |
| Tolerant conversion | `TRY_TO_NUMBER`, `TRY_TO_DATE` (Snowflake) vs `TRY_CAST` (DuckDB) → macro |
| Semi-structured | `VARIANT`, `:field::type`, `LATERAL FLATTEN` |
| Incremental | `materialized='incremental'`, `unique_key`, `incremental_strategy='merge'`, `is_incremental()` filter |
| Cost | Warehouse size, `AUTO_SUSPEND`, avoid `SELECT *` on large tables, query profile |

### Demo (15 min): a dbt model from A to Z

Live, in `default` mode so the room sees every action:

```text
Create a dbt model marts/fct_daily_sales: one row per day and per channel (channel), with the number of
non-cancelled orders and revenue. Start from stg_orders. Add a uniqueness test on the day+channel combination
(singular test or dbt_utils if available, otherwise singular test), document the grain, then run
dbt build --select fct_daily_sales and fix until everything passes.
```

Comment as it runs: Claude reads `stg_orders`, the `parse_amount` macro and `dbt_project.yml`; it **discovers** that `dbt_utils` is not installed and adapts; it executes and fixes.
Show the final diff (`git diff`): **human review is what validates**, not "tests OK".

---

## 2:10 — Exercise 2.2: migrate a Snowflake query to dbt (50 min, pairs)

The query [`sql/legacy/customer_ltv.sql`](../sql/legacy/customer_ltv.sql) (customer lifetime value, LTV) must become a model `marts/dim_customers.sql`.
Required approach: explore and list the problems of the query (Plan Mode) → validate the plan in pairs → implement → `dbt build` → compare the figures with the old logic and **explain every discrepancy**.

### Trainer notes

- Problems to bring out: 5 correlated subqueries on the same table, `nb_orders` including cancelled orders while `total_revenue` excludes them, `total_paid` inflated by multiple order versions, `REPLACE(',', '.')` which does not handle `1 234,50`, a useless `segment IN (...)` filter (all values are in it), non-portable `DATEDIFF`.
- **Deliberate trap**: most pairs will build `dim_customers` on `fct_orders`, which contains the fan-out bug. Their `total_paid` will be wrong and the test `unique_fct_orders_order_id` stays red. If a pair spots it: well done, but we fix it in HD3.
  If nobody spots it, ask at the debrief: "is your `dbt build` entirely green?".
- Solution: [`solutions/dbt_project/models/marts/dim_customers.sql`](../solutions/dbt_project/models/marts/dim_customers.sql) (relies on the corrected `fct_orders`).
- 🚀 For fast finishers: make `fct_orders` incremental (`merge` on `order_id`, filter on `updated_at`).

---

## 3:00 — 4.2 Optimise existing code (15 min)

### Key messages

An optimisation is a **refactoring with unchanged behaviour**. A 4-step method to impose on Claude:

1. **Measure** the existing code (time, memory) and **freeze the reference result** (CSV file or characterisation test);
2. **Diagnose**: where does the time go? (`iterrows`, filters repeated in a loop, `apply(axis=1)`, N queries instead of one);
3. **Rewrite**: pandas vectorisation, joins, or delegate to the SQL engine (DuckDB locally, Snowflake in production);
4. **Prove** that the result is identical (automatic comparison) and measure the gain.

The classic trap: the "optimised" version silently fixes a behaviour of the old one (e.g. which occurrence of a duplicated order is used) and **the figures change without anyone deciding it**. Every divergence must be made explicit and validated.

---

## 3:15 — Exercise 2.3: optimise the legacy report (35 min)

[`src/retail_pipeline/legacy_report.py`](../src/retail_pipeline/legacy_report.py) takes about **90 seconds** on the training dataset.
Goal: under one second, **strictly identical** result, typed and tested code.

### Trainer notes

- Warn them: run the old report only once and save its output (otherwise 90 s are lost on every comparison). A good reflex to have Claude spell out.
- Subtle point: the legacy report takes the **first occurrence** of an order in the file (`iloc[0]`), not the most recent one. A "clean" version that deduplicates on `updated_at` gives different figures. Good discussion: reproduce first, fix afterwards, and say so.
- Solution: [`solutions/src/retail_pipeline/monthly_report.py`](../solutions/src/retail_pipeline/monthly_report.py) (DuckDB, ≈ 0.2 s, zero difference on the 84 rows).

---

## 3:50 — Wrap-up (10 min)

1. Explore before producing, ask for sources to be cited, verify.
2. Grain, dialect and verification criterion in every code request.
3. Optimising = measure, freeze, rewrite, prove.

**Open question for HD3**: "all our tests pass... but are our figures right?"
