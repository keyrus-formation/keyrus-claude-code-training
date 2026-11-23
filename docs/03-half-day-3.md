# Half-day 3 — Make it reliable and equip it

*The session start time is up to the organiser (e.g. 09:00 or 13:30). Timings below are offsets from the start of the 4-hour session.*

**Themes covered**: 5. Testing, debugging & quality · 6. Integrations and automation
**Participant exercises**: [`exercises/HD3_testing_debugging_integrations.md`](../exercises/HD3_testing_debugging_integrations.md)

| Start | Duration | Sequence | Format |
| --- | --- | --- | --- |
| 0:00 | 20 min | 5.1 Testing with an agent: "test first" | Talk |
| 0:20 | 55 min | **Exercise 3.1** — The 4-bug hunt | Individual, group debrief |
| 1:15 | 15 min | 5.2 Data quality and validating generated code | Talk |
| 1:30 | 25 min | **Exercise 3.2** — Python + dbt quality checks | Hands-on |
| 1:55 | 15 min | Break | |
| 2:10 | 25 min | 6.1 Extending Claude Code: the toolbox | Talk |
| 2:35 | 25 min | 6.2 MCP and connections to Data tools | Demo + **Exercise 3.3** |
| 3:00 | 40 min | 6.3 Skills, hooks, automation + **Exercise 3.4** | Demo + hands-on |
| 3:40 | 20 min | Wrap-up and preparation for HD4 | Discussion |

---

## 0:00 — 5.1 Testing with an agent (20 min)

### Key messages

Recall the question left at the end of HD2: **the 4 Python tests pass, and yet the pipeline loses money**.
A green suite only proves what it tests. And an agent that writes code *and* its tests can write tests that validate its own mistakes.

Ground rules with Claude Code:

1. **Test first (TDD — Test-Driven Development)**: "write a test that reproduces the bug, show me it fails, *then* fix it". A test that has never failed has proven nothing.
2. **Edge cases come from you**: French formats, empty values, duplicates, currencies, time zones, split payments. Claude suggests some, you complete them with business knowledge.
3. **Never let a test be modified just to make it pass** unless you decide so explicitly. Put it in `CLAUDE.md`: "never modify an existing test to make it pass; flag it instead".
4. **Forbid workaround behaviours**: `try/except: pass`, silent `errors="coerce"`, a `DISTINCT` that hides a wrong join.
5. **Review the diff**: human review remains the last line of defence. For a fresh pair of eyes, delegate the review to a subagent that has not seen the conversation (the repo provides one: `data-reviewer`).

### Debugging in 4 steps

| Step | Typical prompt |
| --- | --- |
| Reproduce | "here is the symptom: … Write the smallest script or test that reproduces it" |
| Locate | "find the root cause, not the symptom; explain it before proposing a fix" |
| Fix | "fix only the cause, with no unrelated changes" |
| Prove | "the reproduction test passes, the whole suite passes, and here is the quantified impact on the data" |

Provide the raw material: the full error message, the `dbt build` output, a sample of rows. Do not paraphrase.

---

## 0:20 — Exercise 3.1: the 4-bug hunt (55 min)

Brief: the business reports that "revenue doesn't match accounting". Participants have Claude Code, the failing `dbt build` and their `CLAUDE.md`.
For each bug found: a failing test, the fix, the quantified impact.

### The 4 bugs (trainer sheet, do not hand out)

| # | Where | Bug | Impact on the training dataset | Observable symptom |
| --- | --- | --- | --- | --- |
| B1 | `transform.parse_amount` | `'1 234,50'` → the thousands separator (space) is not removed → `ValueError` swallowed → `None` | **366 orders** without an amount, ≈ **€572k** of revenue ignored | Amounts ≥ €1,000 in French format disappear |
| B2 | `transform.clean_orders` | Ascending sort + `keep="first"` → keeps the **oldest** version of the order | **1,000 orders** with a stale status (returns not seen) | Return rate underestimated |
| B3 | `transform.clean_orders` | Division by the rate instead of multiplication (`FX_TO_EUR` = value of one unit in EUR) | **4,058 orders** in USD/CHF wrongly converted | 100 USD → €108.70 instead of €92 |
| B4 | `fct_orders.sql` and `build_order_facts` | Direct join on `payments` (2 payments for some orders) → *fan-out* | **2,796 duplicate rows** in `fct_orders`, revenue inflated by ≈ **€901k** | dbt test `unique_fct_orders_order_id` fails |

Progressive hints if a participant is stuck (every 15 min):
1. "Compare `count(*)` and `count(distinct order_id)` in `fct_orders`."
2. "How many non-empty amounts become `None` after `parse_amount`?"
3. "Take an order that appears twice in `orders.csv`: which status does the pipeline keep?"
4. "100 USD, how much is that in euros?"

### Debrief (10 min)

- How many bugs were found? Which one did Claude find spontaneously, which one thanks to a business question? (Usually B4 is found quickly thanks to the failing dbt test; B1 and B3 thanks to the `CLAUDE.md` enriched in HD1; B2 is the one most often missed.)
- Show that the pitfalls in the model-answer `CLAUDE.md` match the bugs exactly: **business context is what lets the agent find business bugs**.
- Solutions: [`solutions/src/retail_pipeline/transform.py`](../solutions/src/retail_pipeline/transform.py), [`solutions/tests/test_regressions.py`](../solutions/tests/test_regressions.py) (9 tests, 6 of which fail on the original code), [`solutions/dbt_project/models/marts/fct_orders.sql`](../solutions/dbt_project/models/marts/fct_orders.sql).

---

## 1:15 — 5.2 Data quality and validating generated code (15 min)

### Two kinds of tests, two moments

| | Unit tests (pytest) | Data tests (dbt tests, Python checks) |
| --- | --- | --- |
| Verify | That the **code** does what is expected on constructed cases | That the **data** respects the rules on every run |
| Examples | `parse_amount('1 234,50') == 1234.5` | `unique`, `not_null`, `accepted_values`, `relationships`, payments/orders reconciliation |
| When | On every change (CI) | On every load (pipeline, `dbt build`) |

Checks that detect anomalies **in the source** (to be flagged, not silently fixed): 209 negative amounts, 87 orders dated 2031, 212 empty amounts, 2% duplicate customers, upper-case emails.

### Validating generated code: the checklist

1. Existing tests pass, **and** a new test covers the change.
2. The diff touches only what was requested.
3. Key figures are reconciled with an independent source (row counts, checksums).
4. No silent behaviour added (swallowed exception, masking default value).
5. Human review, ideally supported by an independent review (`data-reviewer` subagent, see HD4).

---

## 1:30 — Exercise 3.2: quality checks (25 min)

Complete `quality.py` (4 TODO functions) and add the missing dbt tests, including a singular test reconciling payments with orders.
Solutions: [`solutions/src/retail_pipeline/quality.py`](../solutions/src/retail_pipeline/quality.py), [`solutions/dbt_project/tests/assert_payments_reconcile_with_orders.sql`](../solutions/dbt_project/tests/assert_payments_reconcile_with_orders.sql).

---

## 2:10 — 6.1 Extending Claude Code: the toolbox (25 min)

| Building block | What it is | Loaded when | RetailCo example |
| --- | --- | --- | --- |
| `CLAUDE.md` / rules | Permanent instructions | Always (rules: depending on the files) | Business pitfalls, conventions |
| **Skill** | Reusable procedure (`.claude/skills/<name>/SKILL.md` + supporting files), invoked with `/name` or loaded automatically when its description matches | On demand | `/dbt-model`, `/sql-review`, `/data-quality-audit` |
| **Subagent** | Specialised assistant with its own context, tools and model (`.claude/agents/<name>.md`) | When Claude delegates or when asked | `data-reviewer` (read-only, Sonnet) |
| **Hook** | Shell command run **deterministically** at a point in the cycle (before/after a tool, end of task…) | On every event | `ruff` formatting, blocking secrets and destructive SQL |
| **MCP** (Model Context Protocol) | Standard protocol to plug in external tools (databases, dbt, Jira, GitHub…) | Tools loaded on demand | dbt MCP server, Snowflake-managed MCP server |
| **Plugin** | Package bundling skills, agents, hooks, MCP so they can be shared | At install time | Future "Keyrus Data plugin" |
| **Headless mode** (`claude -p`) | Claude Code on the command line, non-interactive | Scripts, CI, scheduled tasks | Nightly quality report |

Rule of thumb:
- **an instruction to follow most of the time** → `CLAUDE.md`;
- **an occasional multi-step procedure** → skill;
- **a rule that must apply 100% of the time** → hook or `deny` permission;
- **verbose work or work needing fresh eyes** → subagent;
- **an external system** → MCP… or simply its CLI (`gh`, `snow`, `dbt`), often more context-efficient.

The old custom commands (`.claude/commands/*.md`) still work and are now merged with skills.

---

## 2:35 — 6.2 MCP and Data tools (25 min)

### Demo: plugging in the dbt MCP server

The official dbt Labs MCP server (`dbt-mcp`) runs locally with `uvx` and exposes, among other things, model discovery, lineage and dbt command execution.

```bash
claude mcp add dbt \
  -e DBT_PROJECT_DIR="$PWD/dbt_project" -e DBT_PATH="$(which dbt)" -e DBT_PROFILES_DIR="$PWD/dbt_project" \
  -- uvx dbt-mcp
claude mcp list
```

In Claude Code: `/mcp` to see the server status. Then:

```text
with the dbt MCP server, list the models that depend on stg_orders and their tests
```

Installation scopes: `local` (default, only you, this project), `project` (committed `.mcp.json` file, shared with the team — each member approves the server on first use), `user` (all your projects). Configuration template: [`.mcp.json.example`](../.mcp.json.example) (`${VARIABLES}` are read from the environment: no secret in the file).

### Snowflake

Snowflake offers a **managed MCP server** (a `MCP SERVER` object created in the account) that exposes Cortex Analyst, Cortex Search, Cortex agents and SQL execution, with Snowflake's role-based access control (RBAC). Configure it with a **read-only** role for exploration.
Often-sufficient alternative: let Claude use the Snowflake CLI (`snow sql -q ...`) with a restricted role and an `ask` rule in the permissions.

### Cautionary messages

- An MCP server **acts with your rights**: use a test database, a read-only role, never production credentials.
- MCP tool responses enter the context: limit queries that return thousands of rows (Claude Code warns above 10,000 tokens of MCP output).
- Only install servers from known sources (official vendor, Anthropic directory, internal review).

**Exercise 3.3 (15 min)**: plug in `dbt-mcp` and use it to produce the "model → tests → untested columns" matrix.

---

## 3:00 — 6.3 Skills, hooks and automation (40 min)

### Skills demo (10 min)

Open [`.claude/skills/dbt-model/SKILL.md`](../.claude/skills/dbt-model/SKILL.md). Points to show:
- the `description` (it is what triggers automatic loading);
- `$ARGUMENTS`, `allowed-tools` (tools pre-approved while the skill runs);
- [`sql-review`](../.claude/skills/sql-review/SKILL.md): `disable-model-invocation: true` (only via `/sql-review`) and the injection of a `` !`git diff ...` `` command executed before Claude reads the skill;
- [`data-quality-audit`](../.claude/skills/data-quality-audit/SKILL.md): `context: fork` + `agent: Explore` → runs in a read-only subagent, only the report comes back.

Run `/data-quality-audit data/raw/orders.csv` and compare with the anomalies found by hand in 3.2.

### Hooks demo (10 min)

Open [`.claude/settings.json`](../.claude/settings.json) and the scripts in [`.claude/hooks/`](../.claude/hooks):

| Hook | Event | Effect |
| --- | --- | --- |
| `protect-files.sh` | `PreToolUse` on `Edit|Write` | Blocks any write to `.env`, `data/raw/`, `.git/`, `profiles.yml` |
| `block-destructive-sql.sh` | `PreToolUse` on `Bash` | Blocks `rm -rf`, `DROP/TRUNCATE TABLE`, `DELETE` without `WHERE`, dbt on `prod` |
| `format-python.sh` | `PostToolUse` on `Edit|Write` | `ruff format` + `ruff check --fix`; sends remaining errors back to Claude |

How it works: the hook receives a JSON description of the action on standard input; **exit code 2 = action blocked**, and the error message is sent back to Claude, which adapts.
Demo: "drop the raw.orders table in DuckDB" → blocked; Claude explains the block. `/hooks` lists the active hooks.

Key message: **a hook is a guarantee, an instruction in `CLAUDE.md` is a request**.

### Automating recurring tasks (5 min)

Non-interactive mode, for scripts, CI or a scheduled task:

```bash
claude -p "run /data-quality-audit data/raw/orders.csv and write the report to reports/qualite.md" \
  --permission-mode dontAsk \
  --allowedTools "Read" "Edit(./reports/**)" "Bash(python *)" \
  --output-format json > run.json
```

(`reports/qualite.md` is the French file name used by the sample project; it is kept as-is.)

`dontAsk` + a tool allowlist = nothing else can run. Consultant use cases: daily quality report, dbt documentation updates, CI failure triage, automatic PR review (HD4).

### Exercise 3.4 (15 min)

Choose one: write a `/explain-model <model>` skill that documents a dbt model (grain, lineage, tests, untested columns), **or** a `Stop` hook that runs `pytest -q` at the end of each Claude response and sends the failures back to it.

---

## 3:40 — Wrap-up (20 min)

1. Test first, business edge cases, review the diff.
2. Data is tested on every load, code on every change.
3. CLAUDE.md = request; hook/permission = guarantee; skill = procedure; MCP = connection; subagent = separate context.

**For HD4**: everyone pushes their fixes branch to the session repository (without merging).
