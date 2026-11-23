# HD2 — Understanding an existing codebase and producing Data code

Start from your HD1 branch (or from the `state-hd2` branch). Remember to `/clear` between exercises.

---

## Exercise 2.1 — Map RetailCo (35 min)

Goal: produce `docs/ARCHITECTURE.md`, understandable in 5 minutes by a newcomer.

Expected content:
1. a **Mermaid** diagram of the flow: raw CSVs → Python pipeline → DuckDB/Snowflake → staging models → marts;
2. a table of dbt models: name, grain, materialisation, tests;
3. Python dependencies declared vs actually imported;
4. the lineage of `fct_orders` (use `dbt ls --select +fct_orders`);
5. a **"Risk areas"** section (at least 3, with file and line) and an **"Open questions for the business"** section.

Constraint: stay in Plan Mode or `default` mode during exploration; only allow the file `docs/ARCHITECTURE.md` to be written.
Verification: tick in the document every claim that **you** have verified yourself. How many did you find to be inaccurate?

🚀 Going further: ask Claude to use subagents in parallel (one for `src/`, one for `dbt_project/`) and compare the consumption (`/usage`).

---

## Exercise 2.2 — Migrate a Snowflake query to a dbt model (50 min, pairs)

The query [`sql/legacy/customer_ltv.sql`](../sql/legacy/customer_ltv.sql) runs every night on Snowflake. It must become the model `dbt_project/models/marts/dim_customers.sql`.

1. **Explore (Plan Mode)**: have Claude list all the problems of the query (performance, correctness, portability). Add what you had noted yourselves.
2. **Plan**: grain, reused models, columns, tests. Validate the plan as a pair.
3. **Implement**: portable DuckDB/Snowflake SQL (project macros), YAML with description and tests.
4. **Verify**: `cd dbt_project && DBT_PROFILES_DIR=. dbt build --select +dim_customers`.
5. **Compare**: for 5 customers, compare your figures with those of the old logic (run on DuckDB). **Explain every discrepancy** in the model description.

Question to ask yourselves at the end: is your full `dbt build` entirely green?

🚀 Going further: make `fct_orders` incremental (`materialized='incremental'`, `unique_key='order_id'`, `merge` strategy on Snowflake), filtered on `updated_at`.

---

## Exercise 2.3 — Optimise the legacy report (35 min)

[`src/retail_pipeline/legacy_report.py`](../src/retail_pipeline/legacy_report.py) computes monthly revenue by category. It takes about 90 seconds.

Goal: a new module `src/retail_pipeline/monthly_report.py`, under one second, **strictly identical result**.

Required method (give it to Claude):
1. run the old report **only once** and save its output as the reference (`tests/fixtures/monthly_report_reference.csv`);
2. diagnose the causes of slowness;
3. rewrite (vectorised pandas or DuckDB), with typing and docstrings;
4. write a test that compares the new output with the reference;
5. measure the gain.

Underlying question: does the old report make a questionable business choice on orders that appear several times? Should it be reproduced or fixed? Who decides?
