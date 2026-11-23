# Half-day 1 — Getting started with Claude Code

**Themes covered**: 1. Introduction and fundamentals · 2. Prompting & context engineering
**Participant exercises**: [`exercises/HD1_getting_started.md`](../exercises/HD1_getting_started.md)

The session start time is up to the organiser (e.g. 09:00 or 13:30); the plan below uses elapsed time from the start (4 hours in total).

| Elapsed | Duration | Sequence | Format |
| --- | --- | --- | --- |
| 0:00 | 15 min | Welcome, round table, expectations | Discussion |
| 0:15 | 35 min | 1.1 From chat assistant to agent | Talk + demo |
| 0:50 | 30 min | 1.2 Installation, configuration, permissions | Demo + practice |
| 1:20 | 30 min | **Exercise 1.1** — First contact with RetailCo | Individual practice |
| 1:50 | 15 min | Break | |
| 2:05 | 30 min | 2.1 Writing effective instructions | Talk + **Exercise 1.2** |
| 2:35 | 25 min | 2.2 Context: window, `CLAUDE.md`, memory | Talk + demo |
| 3:00 | 30 min | **Exercise 1.3** — Write the project's `CLAUDE.md` | Practice |
| 3:30 | 20 min | 2.3 Plan Mode and decomposition + **Exercise 1.4** | Demo + practice |
| 3:50 | 10 min | Wrap-up, questions, preparing half-day 2 | Discussion |

---

## 0:00 — Welcome (15 min)

Round table, one sentence each: role, usual stack (SQL/dbt/Python/Spark…), current AI usage (none / ChatGPT / Copilot / Cursor / Claude Code).
Note the "already users" profiles on the board: they will act as reference buddies.

Set the ground rules: 50% practice, one running project, we break things on purpose, and we never work on real client data during the training.

---

## 0:15 — 1.1 From chat assistant to agent (35 min)

### Key messages

**An LLM (Large Language Model) in chat mode** receives text and returns text. You are the one who copies the code, runs it, and pastes the error back.
**An agent** receives a goal, then **loops**: it gathers context, acts with tools, checks the result, and starts again until the goal is reached (or it needs you).

```
            ┌──────────────────────────────────────────┐
   goal  →  │ 1. Gather context (read, search)          │
            │ 2. Act (edit, run a command)              │ ← you can interrupt (Esc)
            │ 3. Verify (tests, output, errors)         │   and redirect at any time
            └──────────────┬───────────────────────────┘
                           └── loops until "done" or a question to the human
```

| | Chat assistant | Agent (Claude Code) |
| --- | --- | --- |
| Access to code | What you paste | The whole repository, on demand |
| Execution | None | Shell commands, tests, dbt, git |
| Verification | By you | By itself, if you give it the means |
| Unit of work | One answer | One task (dozens of actions) |
| Main risk | Wrong answer | Wrong **action** (overwritten file, dangerous command) |
| Your role | Question writer | **Project manager + reviewer** |

**Claude Code's tools** (show them in the demo, without going into detail): file reading, search (`Grep`, `Glob`), editing (`Edit`, `Write`), execution (`Bash`), web (`WebFetch`, `WebSearch`), delegation to subagents, and all extensions (MCP, skills) covered in half-day 3.

**Where Claude Code is used**: terminal (the core of the training), VS Code and JetBrains extensions, desktop app, web (claude.ai/code), Slack, GitHub Actions / GitLab CI. Same engine, same configuration files.

### Demo (10 min)

In the RetailCo repository, default mode, prompt projected on screen:

```text
que fait ce projet ? donne-moi l'architecture en 5 lignes et la commande pour tout lancer
```

(French for: "what does this project do? give me the architecture in 5 lines and the command to run everything". The sample project and its data are French, so French prompts are fine.)

Comment live: **Claude received nothing but the question**; it decides on its own to read the README and `pyproject.toml` and to list `src/`. Point out the tool calls displayed.

Then:

```text
lance les tests unitaires et dis-moi s'ils passent
```

(French for: "run the unit tests and tell me whether they pass".)

Claude asks permission to run `pytest` (or not, if the project's `allow` rule covers it — a good opportunity to introduce the permissions section).

### Trainer notes

- Frequent question: "which model is running behind the scenes?" → `/model` lets you choose (Opus for complex reasoning, Sonnet by default for most coding tasks, Haiku for simple, fast tasks). We come back to costs in half-day 4.
- Do not promise that the agent "understands" the business: it infers from what it reads. Hence the importance of `CLAUDE.md` (after the break).

---

## 0:50 — 1.2 Installation, configuration, permissions (30 min)

### Installation (reminder: normally done beforehand)

```bash
# macOS, Linux, WSL (native install recommended, automatic updates)
curl -fsSL https://claude.ai/install.sh | bash
# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
# Alternatives: brew install --cask claude-code   |   winget install Anthropic.ClaudeCode
claude --version
```

On native Windows, Git for Windows is recommended (otherwise Claude Code uses PowerShell as its shell). WSL does not need it.

Sign-in happens on the first launch of `claude`: Claude account (Pro, Max, Team, Enterprise), Claude Console (API), or cloud provider (Amazon Bedrock, Google Cloud, Microsoft Foundry).

### Essential commands (on the cheat sheet)

| Command | Effect |
| --- | --- |
| `claude` / `claude "task"` | Interactive session (with a first prompt) |
| `claude -p "question"` | Non-interactive (*headless*) mode: answers then exits — the basis for automation (half-days 3/4) |
| `claude -c` / `claude -r` | Resume the last conversation / pick a conversation |
| `/help`, `/` | List of available commands and skills |
| `/clear` | Start again from an empty context |
| `/model`, `/effort` | Choose the model and the thinking level |
| `/usage`, `/context` | Consumption and context window usage |
| `Esc` | Interrupt Claude; `Esc` ×2 or `/rewind`: go back to a checkpoint |
| `Shift+Tab` | Cycle through the permission modes |
| `@path/file` | Reference a file in the prompt |
| `!command` | Run a shell command yourself |

### Permission modes

| Mode | What runs without asking | Use |
| --- | --- | --- |
| `default` ("Manual") | Reads only | Discovery, sensitive client code — **the training mode** |
| `acceptEdits` | Reads + file edits + common file commands in the folder | Iterating on code you review as you go |
| `plan` | Reads (exploration), no modifications | Analyse and plan before touching the code |
| `auto` | Everything, with a background safety classifier | Long tasks, if available and allowed |
| `dontAsk` | Reads + pre-approved tools; everything else is denied | CI and locked-down scripts |
| `bypassPermissions` | Everything | **Only** in an isolated container or VM (virtual machine) |

Points to stress:
- `deny` rules apply **in every mode**, including `bypassPermissions`.
- Writes to `.git`, `.claude`, `.mcp.json`… are never auto-approved (except in `bypassPermissions`).

### Demo: the repository's configuration files

Open [`.claude/settings.json`](../.claude/settings.json) and read it with the room:

- `allow`: pytest, ruff, local dbt, read-only git → no friction on safe actions;
- `ask`: `git commit`, `git push`, dbt on the Snowflake target → human confirmation;
- `deny`: reading `.env` and credential profiles, modifying `data/raw/`, `curl`/`wget`.

Priority order of settings: **managed** (enforced by IT) > command line > `.claude/settings.local.json` (personal, not committed) > `.claude/settings.json` (team, committed) > `~/.claude/settings.json` (user).

Live demonstration: `lis le fichier .env` ("read the .env file") → refused. This is the first building block of the security part (half-day 4).

---

## 1:20 — Exercise 1.1: first contact with RetailCo (30 min)

See the exercise sheet. Goal: **everyone** has a working session, has seen Claude read, execute and answer, and has met a permission request.

Walk the room: unblock failed installations first. After 20 min, have 2 or 3 people share their answers to "what surprised you?".

---

## 2:05 — 2.1 Writing effective instructions (30 min)

### Key messages

A good prompt for an agent is not an incantation, it is **a good Jira ticket**: context, goal, constraints, definition of done.

| Principle | Bad | Good |
| --- | --- | --- |
| Be specific | "fix the bug" | "in `transform.clean_orders`, duplicate orders keep the old version: keep the one with the most recent `updated_at`" |
| Point to files | "look at the orders model" | "look at `@dbt_project/models/marts/fct_orders.sql`" |
| Give a verification criterion | "add tests" | "add a test that fails on the current code, then fix it, then run `pytest -q` until everything passes" |
| Set constraints | — | "without adding a dependency", "SQL compatible with Snowflake and DuckDB", "do not change the public API" |
| Give an example | "format the amounts" | "`'1 234,50'` → `1234.5`, `''` → `None`" |
| One task at a time | "rebuild the pipeline and the docs and the tests" | three successive requests, with verification between each |
| Let it explore first | "implement X" | "read the relevant code and explain how X should fit in, do not modify anything" |

Formula to remember: **Context → Goal → Constraints → Verification**.

Other levers:
- paste a full error or a screenshot rather than paraphrasing it;
- ask Claude to **ask you questions** before starting when the need is vague ("interview me about what is missing");
- correct early: `Esc` as soon as the direction is wrong, rather than letting it finish.

### Exercise 1.2 (15 min, built in)

Participants rewrite 3 weak prompts from the exercise sheet, test them, and compare the number of actions and the quality of the result. Debrief: have the best prompt in the room read aloud.

---

## 2:35 — 2.2 Context: window, `CLAUDE.md`, memory (25 min)

### The context window

Everything Claude "knows" during a session fits in its context window: system instructions, `CLAUDE.md`, history, contents of files read, command outputs. It is large, but:
- the fuller it gets, the more each exchange costs (everything is sent again with every request);
- old, off-topic information dilutes attention.

Habits to adopt:

| Habit | When |
| --- | --- |
| `/context` | See what fills the window |
| `/clear` | Between two unrelated tasks (free) — `/rename` first to find the session again |
| `/compact instruction` | Summarise a long session while keeping the essentials (e.g. `/compact keep the modified files and the test results`) |
| Subagents | Delegate verbose tasks (search, logs): only the summary comes back (half-day 3) |

### `CLAUDE.md`: the project's memory

Every session starts blank. `CLAUDE.md` is a Markdown file **loaded automatically at startup** that provides permanent instructions.

| Location | Scope | Committed? |
| --- | --- | --- |
| Company policy (`/etc/claude-code/CLAUDE.md` on Linux…) | The whole organisation, enforced by IT | — |
| `~/.claude/CLAUDE.md` | You, all your projects | No |
| `./CLAUDE.md` (or `./.claude/CLAUDE.md`) | The project, the whole team | **Yes** |
| `./CLAUDE.local.md` | You, this project (add to `.gitignore`) | No |
| `subfolder/CLAUDE.md` | Loaded when Claude works in that subfolder | Yes |
| `.claude/rules/*.md` with `paths:` | Loaded only for matching files | Yes |

All files found are **concatenated** (no replacement). A file can import another with `@path/file`.
There is also an **automatic memory** that Claude writes itself from your corrections; `/memory` lets you view and edit everything.

**What goes in `CLAUDE.md`**: what Claude cannot guess by reading the code.
- exact build/test commands;
- business pitfalls ("amounts arrive in French format", "an order can have 2 payments");
- team conventions (dbt naming, commit format);
- prohibitions ("never run dbt on prod").

**What does not belong there**: a description of every file (Claude can read), long and rare procedures (→ skills, half-day 3), rules that must be **guaranteed** (→ `deny` permissions or hooks: `CLAUDE.md` is context, not a constraint).
Aim for **fewer than 200 lines**; beyond that, adherence drops and cost rises.

### Demo (5 min)

Show [`.claude/rules/dbt.md`](../.claude/rules/dbt.md): thanks to `paths:`, these rules enter the context only when Claude touches a dbt file.

---

## 3:00 — Exercise 1.3: write the project's `CLAUDE.md` (30 min)

1. `/init` generates a first version from the code.
2. Participants critique and enrich it with the **business pitfalls** they have discovered (or find by questioning Claude about the data).
3. Test: `/clear`, then a trick question ("how is the amount in euros calculated?") to check that the context is used.

Reference solution: [`solutions/CLAUDE.md`](../solutions/CLAUDE.md). **Do not show it before the end**: the point is to see that `/init` does not find the business pitfalls on its own.
The pitfalls listed in the solution are exactly the bugs hunted in half-day 3: this is intentional, and we will come back to it.

---

## 3:30 — 2.3 Plan Mode and decomposition (20 min)

### Key messages

Plan Mode (`Shift+Tab` until "plan", or `claude --permission-mode plan`): Claude **explores and proposes a plan without modifying anything**. You approve, amend or reject before any write.

Recommended workflow for any non-trivial task: **Explore → Plan → Implement → Verify → Commit**.

- Explore: "read X and Y, explain how it works, do not modify anything".
- Plan: Plan Mode, a step-by-step plan with impacted files and planned tests. Add "think deeply" for complex topics.
- Implement: leave Plan Mode, step by step, verifying after each step.
- Verify: tests, `dbt build`, review the diff.

Decompose: one task = one verifiable result. A 15-step plan is split into 3 sessions with `/clear` between them, the plan being saved in a file (`PLAN.md`).

### Exercise 1.4 (15 min)

Add to the pipeline a `--since YYYY-MM-DD` option that loads only orders after a given date. **Plan Mode is mandatory**, and the plan must be approved by your buddy before implementation.

---

## 3:50 — Wrap-up (10 min)

Have the room state the 3 ideas they retain. Complete with:
1. the agent acts → permissions and review;
2. context = quality and cost → short `CLAUDE.md`, `/clear` often;
3. Plan Mode before coding.

**For half-day 2**: keep your `CLAUDE.md`; those who wish read the query [`sql/legacy/customer_ltv.sql`](../sql/legacy/customer_ltv.sql) (without Claude!) and note what looks suspicious.
