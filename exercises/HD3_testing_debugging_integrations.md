# HD3 — Make it reliable and equip it

Create a `fix/<your-name>` branch before you start.

---

## Exercise 3.1 — The bug hunt (55 min)

> Message from management control: "Revenue in the `fct_orders` table is higher than in accounting,
> and yet some large B2B orders show no amount at all. The dollar amounts look odd too.
> And the return rate is much lower than what customer service sees."

The Python pipeline (`src/retail_pipeline/transform.py`) and the dbt model `fct_orders` contain **several bugs**.
All existing unit tests pass.

For **each** bug you find:
1. write (or have Claude write) a test that **fails** on the current code — show the failure;
2. find the root cause and fix it, with no unrelated changes;
3. verify: `pytest -q` and `dbt build`;
4. quantify the impact on the data (rows and euros affected);
5. commit separately: `fix(scope): description`.

Rules: you must not modify an existing test to make it pass, add a `DISTINCT` to hide a duplicate, or swallow an exception.

Keep this table up to date:

| # | File / function | Cause | Test added | Impact |
| --- | --- | --- | --- | --- |
| | | | | |

---

## Exercise 3.2 — Quality checks (25 min)

1. Run `/data-quality-audit data/raw/orders.csv`. Compare with what you already know.
2. Complete the 4 functions marked `TODO` in [`src/retail_pipeline/quality.py`](../src/retail_pipeline/quality.py), with their unit tests.
3. On the dbt side, add:
   - a `relationships` test from `fct_orders.customer_id` to `stg_customers`;
   - a **singular test** `dbt_project/tests/assert_payments_reconcile_with_orders.sql` that checks that the amount paid in `fct_orders` equals the sum of the raw payments.
4. Source anomalies (negative amounts, future dates, empty emails) must be **flagged**, not deleted. Where and how do you flag them?

---

## Exercise 3.3 — Plug in the dbt MCP server (15 min)

Prerequisite: `uv` installed.

```bash
claude mcp add dbt \
  -e DBT_PROJECT_DIR="$PWD/dbt_project" -e DBT_PATH="$(which dbt)" -e DBT_PROFILES_DIR="$PWD/dbt_project" \
  -- uvx dbt-mcp
```

1. In Claude Code, run `/mcp`: is the server connected? Which tools does it offer?
2. Using the MCP server, produce the matrix: model → tests → **untested** columns.
3. Compare with the same request made without MCP (`/mcp` to disable it): result, number of actions, consumption (`/usage`).

---

## Exercise 3.4 — Your own automation (15 min)

Choose one:

**A. A skill** `/explain-model <model>` in `.claude/skills/explain-model/SKILL.md` that documents a dbt model: grain, upstream/downstream lineage, tests, untested columns, and suggests the missing tests. Test it on `fct_orders` and `stg_orders`.

**B. A `Stop` hook** in `.claude/settings.json` that runs `pytest -q` at the end of each Claude response and, on failure, sends the failing tests back to it (exit code 2). Beware of infinite loops: what happens if the tests stay red? (The JSON received by the hook contains `stop_hook_active`.)

**C. A non-interactive script** `scripts/nightly_quality.sh` that calls `claude -p` in `dontAsk` mode with a tool allowlist to produce `reports/qualite.md` (a French file name from the sample project, kept as-is).
