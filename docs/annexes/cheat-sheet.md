# Claude Code Cheat Sheet — Keyrus Data Consultants

## Launch

| Command | Effect |
| --- | --- |
| `claude` | Interactive session in the current folder |
| `claude "task"` | Session starting with a first prompt |
| `claude -p "question"` | Non-interactive mode (scripts, CI) — `--output-format json` |
| `claude -c` / `claude -r` | Resume the last session / pick one |
| `claude --permission-mode plan` | Start in Plan Mode |

## In the session

| Command / key | Effect |
| --- | --- |
| `/` | Available commands and skills |
| `Shift+Tab` | Switch mode: `default` → `acceptEdits` → `plan` (→ `auto` if available) |
| `Esc` | Interrupt; `Esc` ×2 or `/rewind`: go back to a checkpoint |
| `@file` | Put a file in the context |
| `!command` | Run a shell command yourself |
| `/clear` | Empty the context (between two tasks) — `/rename` first to find the session again |
| `/compact instruction` | Summarise the session, keeping the essentials |
| `/context`, `/usage` | Context occupancy, consumption and recommendations |
| `/model`, `/effort` | Choose the model, the thinking level |
| `/init`, `/memory` | Create or edit `CLAUDE.md` and memory |
| `/permissions`, `/hooks`, `/mcp` | Inspect permissions, hooks, MCP servers |
| `/code-review`, `/security-review` | Code review / security review of the changes |

## Phrase it well: Context → Goal → Constraints → Verification

> "In `@dbt_project/models/marts/fct_orders.sql` (context), guarantee one row per order (goal),
> without changing the exposed columns and in SQL portable across DuckDB/Snowflake (constraints). Add a test that fails before
> the fix, then run `dbt build --select fct_orders+` until everything passes (verification)."

## Workflow: Explore → Plan → Implement → Verify → Commit

## What goes where

| Need | Tool |
| --- | --- |
| Permanent instruction, business pitfall | `CLAUDE.md` (< 200 lines); targeted rules: `.claude/rules/*.md` with `paths:` |
| Personal preference | `~/.claude/CLAUDE.md`, `CLAUDE.local.md` |
| Reusable procedure | Skill: `.claude/skills/<name>/SKILL.md` → `/name` |
| Fresh eyes, verbose task | Subagent: `.claude/agents/<name>.md` |
| Rule that must hold 100% of the time | `deny` permission or hook (`exit 2` = blocked) |
| External tool (dbt, Snowflake, Jira…) | MCP: `claude mcp add …` — or the tool's CLI |

## Golden rules on assignment

1. **Commercial** Keyrus account only; never a personal account on client code.
2. No secrets or production credentials on the machine; `.env` in `deny`.
3. Explore with a **read-only** role; aggregates rather than data rows.
4. Plan Mode before any non-trivial task; a failing test before any fix.
5. I read every diff; **I sign what I deliver**.
6. `/clear` often, Sonnet by default, precise prompts: context costs money.
