# Half-day 4 — Industrialize, secure, deliver

**Themes covered**: 7. Industrialization and delivery · 8. Security, governance and costs · 9. End-to-end case study
**Participant exercises**: [`exercises/HD4_industrialization_case_study.md`](../exercises/HD4_industrialization_case_study.md)

> The session start time is up to the organiser (e.g. 09:00 or 13:30). Timings below are offsets from the start of the 4-hour session.

| Offset | Duration | Sequence | Format |
| --- | --- | --- | --- |
| 0:00 | 30 min | 7.1 Git, code reviews and CI/CD with Claude Code | Talk + demo |
| 0:30 | 20 min | **Exercise 4.1** — From branch to reviewed PR | Hands-on |
| 0:50 | 15 min | 7.2 Reusability and collaboration between consultants | Talk |
| 1:05 | 35 min | 8. Security, governance, costs | Talk + demo |
| 1:40 | 15 min | Break | |
| 1:55 | 95 min | **Exercise 4.2 — End-to-end case study** (pairs) | Guided hands-on |
| 3:30 | 20 min | Presentations (3 pairs × 5 min) + debrief | Discussion |
| 3:50 | 10 min | Quiz, feedback survey, closing | Individual |

---

## 0:00 — 7.1 Git, code reviews and CI/CD (30 min)

### Claude Code and Git

Claude handles Git like a developer: `git status`, branches, commits, conflict resolution, and PRs via the `gh` CLI.

Recommended team rules (already in place in `.claude/settings.json`):
- `git status`, `git diff`, `git log` allowed without confirmation; **`git commit` and `git push` set to `ask`**;
- one branch per task; never commit directly to `main`;
- commit messages in the team format (written in `CLAUDE.md`), with one line of "why" context;
- **small PRs**: one PR = one intent, reviewable in 10 minutes.

To work in parallel without stepping on each other: **Git worktrees** (`git worktree add ../retailco-feature-x -b feature-x`), one Claude Code session per worktree.

### The three review levels

| Level | Tool | What it brings |
| --- | --- | --- |
| 1. Guided self-review | `/sql-review file.sql`, explicit request "review your diff" | Fast, but the agent reviews its own work |
| 2. Independent review | Subagent [`data-reviewer`](../.claude/agents/data-reviewer.md) (clean context, read-only, Sonnet), built-in skills `/code-review`, `/security-review` | Fresh eyes, free of the conversation's bias |
| 3. Human review | GitHub/GitLab PR | **Mandatory**: the consultant signs off on what they deliver |

Key message: levels 1 and 2 **prepare** the human review, they do not replace it.

### CI/CD: Claude Code in GitHub Actions

Two workflows in the repository:
- [`ci.yml`](../.github/workflows/ci.yml): classic CI (ruff, pytest, data generation, `dbt build` on DuckDB). Claude does not take part: **CI must stay deterministic**.
- [`claude.yml`](../.github/workflows/claude.yml): official action `anthropics/claude-code-action@v1`,
  - interactive mode: a comment such as `@claude fix the failing dbt test` in a PR or issue triggers Claude;
  - automatic mode: on every PR, a review with a given instruction and a tool allowlist (`--allowedTools`), capped by `--max-turns` and a `timeout-minutes`.

Setup: `/install-github-app` from Claude Code (installs the GitHub app, creates the secret, opens the workflow PR), or manually (Claude GitHub app + `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN` secret + copy the workflow).
On GitLab: equivalent CI/CD integration (see the Claude Code documentation, "GitLab CI/CD").

### Demo (10 min)

1. `git checkout -b fix/fan-out-fct-orders`; ask Claude to fix the fan-out with a test;
2. `use the data-reviewer subagent to review my changes` → verdict;
3. "create the PR with gh, description in English: context, fix, quantified impact, tests";
4. on GitHub: CI runs, the automatic review posts its comment; an `@claude` in the PR to ask a question.

---

## 0:30 — Exercise 4.1: from branch to reviewed PR (20 min)

Each participant turns their Half-day 3 fixes into **one clean PR**: branch, atomic commits, `data-reviewer` review, generated then proofread PR description, green CI.

---

## 0:50 — 7.2 Reusability and collaboration (15 min)

What gets shared, and how:

| What | Where | Shared with |
| --- | --- | --- |
| Project instructions, permissions, hooks, skills, subagents, rules | `CLAUDE.md`, `.claude/` in the repository | The project team (via Git) |
| Personal preferences | `~/.claude/`, `CLAUDE.local.md`, `.claude/settings.local.json` | Nobody |
| Project MCP servers | `.mcp.json` (no secrets, environment variables) | The project team |
| Keyrus cross-project know-how (`dbt-model` skill, SQL review, quality audit) | Internal **plugin** published on a Keyrus Git *marketplace* | All consultants |
| Enforced rules (prohibitions, allowed models) | *Managed settings* deployed by IT | The whole organization |

Proposal to discuss with the room: a Keyrus **mission starter kit** = a template repository containing a standard `CLAUDE.md`, a secure `.claude/settings.json`, hooks, Data skills, and the security checklist below. Each mission copies it, then enriches it with the client's business pitfalls.

Collaboration best practices:
- `CLAUDE.md` is reviewed in PRs like code; a correction made to Claude twice → one line in `CLAUDE.md`;
- document useful sessions: `/rename` + a summary in the PR (prompt, decisions, checks);
- capitalize: a skill that proved useful on 2 missions moves into the Keyrus plugin.

---

## 1:05 — 8. Security, governance and cost control (35 min)

### 8.1 Client data confidentiality (15 min)

**What is sent to Anthropic**: Claude Code runs locally, but everything that enters the context (prompts, content of files read, command outputs, **including data rows** if Claude runs a `select *`) is sent to the model, encrypted in transit (TLS 1.2+).

**What Anthropic does with it** (Claude Code documentation, *Data usage* page, November 2026):

| | Commercial accounts (Team, Enterprise, API, cloud platforms) | Consumer accounts (Free, Pro, Max) |
| --- | --- | --- |
| Model training | **No**, unless voluntarily opted in (partner program) | Depends on the user's chosen setting |
| Retention | 30 days; **ZDR** (Zero Data Retention, no retention) possible on Claude for Enterprise after eligibility validation | 30 days, or 5 years if the user accepted use for training |
| Locally | Plain-text transcripts in `~/.claude/projects/` for 30 days (`cleanupPeriodDays`) | Same |

**Keyrus rule to set: commercial accounts only for client code or data. Never a personal account.**
Also check what the client's contract allows: some clients require hosting in their own cloud (Bedrock, Google Cloud, Foundry), others prohibit any generative AI tool.

Concrete measures on a mission:

| Risk | Measure |
| --- | --- |
| Reading secrets | `deny` on `.env`, dbt profiles, `~/.snowflake`; secrets in a vault, never in the repository |
| Personal data in the context | Work on anonymized or synthetic samples; instruction "aggregates only, 20 rows max"; Snowflake role without access to sensitive columns (dynamic masking) |
| Destructive action | Read-only role for exploration; blocking hooks; never production credentials on the workstation |
| Prompt injection (malicious instructions hidden in a file, a web page, a data value) | `default` mode on untrusted content; do not pipe untrusted content; `curl`/`wget` set to `deny`; sandbox (`/sandbox`) to isolate the file system and network |
| Leak through telemetry / feedback | Commercial accounts; `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` variable if the client requires it; do not use `/feedback` on client code |
| Local copy of sessions | Reduce `cleanupPeriodDays`; workstation disk encryption |

### 8.2 Human oversight and AI-related risks (10 min)

Risks to name explicitly:
- **plausible but wrong code** (the 4 bugs of Half-day 3 could have been written by an AI);
- **overconfidence**: the better the tool, the less we review;
- **scope drift**: the agent "improves" files it was not asked to touch;
- **test circumvention**: changing the test rather than the code;
- **dependence**: a consultant who no longer understands the code they deliver.

Safeguards: Plan Mode before any non-trivial task, `default` or `acceptEdits` mode (no `bypassPermissions` outside a container), tests written or validated by a human, independent review, **PR reviewed and signed off by a human**, traceability (PR description that mentions the use of Claude and the checks performed).

For the enterprise: *managed settings* (enforced prohibitions, ability to disable `bypassPermissions` and `auto` mode), enterprise `CLAUDE.md`, usage tracking via OpenTelemetry, `ConfigChange` hooks to audit configuration changes.

### 8.3 Optimizing consumption (10 min)

Benchmarks (Claude Code documentation, *Manage costs* page): about $13 per developer per active day, $150–250 per month, under $30 per active day for 90% of users.

Cost is proportional to **the volume of context processed**: every exchange resends the whole conversation.

| Lever | Action |
| --- | --- |
| Context | `/clear` between two tasks; `/compact` with instructions; `CLAUDE.md` < 200 lines; long procedures as skills (loaded on demand) |
| Model | Sonnet by default; Opus for architecture and hard reasoning; Haiku for simple subagents (`model: haiku`); lower `/effort` on simple tasks |
| Prompts | Specific ("in `auth.ts`…") rather than "improve the repo", which triggers massive reading |
| Tools | CLI (`gh`, `dbt`, `snow`) rather than MCP when equivalent; disable unused MCP servers (`/mcp`); hooks that filter verbose output (return only failing tests) |
| Delegation | Subagents for voluminous output (logs, tests): only the summary comes back |
| Method | Plan Mode to avoid coding in the wrong direction; `Esc` early; test in small increments |
| Monitoring | `/usage` (session, breakdown by skill/subagent/MCP, recommendations), `/context`, `/insights`; organization side: spending limits, admin dashboards |

On the Snowflake side, do not forget **the compute cost triggered by the agent**: dedicated XS warehouse, `AUTO_SUSPEND = 60`, resource monitor (see [`snowflake/setup_training_env.sql`](../snowflake/setup_training_env.sql)).

### Demo (5 min)

`/usage` then `/context` at the end of a demo session: read the breakdown (files read, MCP tools, `CLAUDE.md`) and the recommendations together with the room.

---

## 1:55 — Exercise 4.2: end-to-end case study (95 min, pairs)

### The requirement (to be read aloud)

> RetailCo's sales leadership wants to **identify, every month, customers at risk of churning** in order to trigger a retention campaign.
> A customer is "at risk" if they have placed no non-cancelled order for **more than 90 days** (**60 days** for VIPs), while having placed **at least 2 orders** in the preceding 12 months.
> Deliverables: a dbt table the BI team can use, and a daily CSV export for the CRM (Customer Relationship Management) tool **with no personal data in clear text**.

### Required steps and milestones

| Milestone | Indicative time | Expected | Theme |
| --- | --- | --- | --- |
| 1. Scoping | 10 min | Questions to the "business" (the trainer), assumptions written in `docs/cas_pratique.md`: reference date, statuses retained, grain | 2 |
| 2. Exploration and plan | 15 min | Plan Mode: existing models reused, new files, planned tests. Plan validated by the trainer | 2, 3 |
| 3. dbt model | 25 min | `marts/mart_customers_at_risk.sql` + documented and tested YAML, `dbt build` green | 4, 5 |
| 4. Python export | 20 min | `src/retail_pipeline/export_at_risk.py` + pytest tests; pseudonymized email (hashing) | 4, 5, 8 |
| 5. Delivery | 15 min | Branch, `data-reviewer` review, PR with description, CI green | 7 |
| 6. Cost review | 5 min | `/usage` readout for the session, one improvement to `CLAUDE.md` or one proposed skill | 6, 8 |

(`docs/cas_pratique.md` is the file name used in the sample project, kept as-is; "cas pratique" means "case study".)

### "Business" answers (give only if asked — that is the point of milestone 1)

- Reference date: parameter `as_of_date`, default **2026-09-01** (the data stops at the end of August 2026);
- orders taken into account: statuses `delivered`, `shipped`, `returned` (not `cancelled`); future dates are ignored;
- "preceding 12 months" = the 365 days before `as_of_date`;
- grain: one row per customer, **all** customers (with a boolean `is_at_risk`);
- export: only at-risk customers, columns `customer_key` (SHA-256 of the normalized email), `segment`, `days_since_last_order`, `orders_last_12m`, `revenue_last_12m`; no name, no clear-text email.

### Evaluation grid

See [annexes/evaluation.md](annexes/evaluation.md). Solution: [`solutions/dbt_project/models/marts/mart_customers_at_risk.sql`](../solutions/dbt_project/models/marts/mart_customers_at_risk.sql) and [`solutions/src/retail_pipeline/export_at_risk.py`](../solutions/src/retail_pipeline/export_at_risk.py).

### Trainer notes

- Reference result (solution, `as_of_date = 2026-09-01`): **665 at-risk customers** out of 2,000 (291 VIP, 202 B2B, 172 B2C);
  **641 exported**, 24 being excluded for lack of an email. A gap of a few dozen usually comes from a different assumption (statuses, 365-day boundary).
- Walk around the pairs at milestone 2: **refuse a plan without tests or an explicit grain**.
- Frequent pitfalls: forgetting the VIP threshold; counting cancelled orders; using `current_date` (non-reproducible result); joining the uncorrected `fct_orders` (fan-out); exporting the email in clear text "just to test"; hashing without normalization (case, spaces); future dates that yield a negative `days_since_last_order`.
- If a pair finishes early: make the model incremental, or add a scheduled GitHub Action that produces the export.

---

## 3:30 — Presentations (20 min)

Three pairs, 5 minutes each: the initial plan, what Claude did well, what had to be corrected, the session cost.
Debrief: compare the definitions chosen (differences in figures almost always come from different assumptions, not bugs).

## 3:50 — Closing (10 min)

- 10-question quiz ([annexes/evaluation.md](annexes/evaluation.md));
- feedback survey;
- hand over the [cheat sheet](annexes/cheat-sheet.md) and repository access (`solutions` branch open to everyone).
