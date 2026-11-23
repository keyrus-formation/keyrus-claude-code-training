# Trainer Guide — Claude Code for Data Consultants (Keyrus)

> A **4 half-day training (4 × 3 h 45 of face-to-face, 15 h in total)**. A half-day is either a morning or an
> afternoon: the start time is up to the organiser. It is aimed at Data consultants of mixed levels: some have
> never used an AI agent, others already know GitHub Copilot, Cursor or Claude Code. The running thread is the
> **RetailCo** project in this repository (Python, SQL, dbt, DuckDB locally, Snowflake optional).

## Learning objectives

By the end of the training, each participant can:

1. explain what an AI (artificial intelligence) agent is and how it differs from an LLM (Large Language Model) used in chat mode;
2. install, configure and drive Claude Code (permission modes, Plan Mode, context management);
3. write effective instructions and maintain a useful project `CLAUDE.md`;
4. explore and document an unfamiliar Data repository (architecture, lineage, dependencies) in under an hour;
5. produce tested SQL, Python and dbt code with Claude Code, portable across DuckDB / Snowflake;
6. detect and fix data bugs (fan-out, deduplication, formats) with a "test first" approach;
7. extend Claude Code with MCPs (Model Context Protocol), Skills, hooks and subagents;
8. integrate Claude Code into a Git / CI/CD (continuous integration / continuous delivery) flow with human review;
9. apply the rules on customer data privacy, governance and cost control.

## Schedule

| Half-day | Themes | Running thread | File | Slides |
| --- | --- | --- | --- | --- |
| **1** — Getting started | 1. Fundamentals · 2. Prompting & context engineering | Installation, first contact with RetailCo, `/init`, writing the `CLAUDE.md`, Plan Mode | [01-half-day-1.md](01-half-day-1.md) | [half-day-1.pptx](../slides/half-day-1.pptx) |
| **2** — Understand and produce | 3. Code exploration · 4. AI-assisted Data development | Repository mapping, migrating a Snowflake query to dbt, optimising a pandas script (90 s → 0.2 s) | [02-half-day-2.md](02-half-day-2.md) | [half-day-2.pptx](../slides/half-day-2.pptx) |
| **3** — Make it reliable and equipped | 5. Testing, debugging & quality · 6. Integrations & automation | Hunt for the 4 hidden bugs (≈ €570k of revenue lost), quality tests, dbt MCP, Skills, hooks | [03-half-day-3.md](03-half-day-3.md) | [half-day-3.pptx](../slides/half-day-3.pptx) |
| **4** — Industrialise | 7. Delivery · 8. Security, governance, costs · 9. End-to-end case study | PR (pull request) reviewed by a subagent and by CI, "at-risk customers" case study in pairs | [04-half-day-4.md](04-half-day-4.md) | [half-day-4.pptx](../slides/half-day-4.pptx) |

Theme 9 (hands-on practice) is not concentrated in half-day 4: **each half-day devotes about 50% of its time to exercises** on RetailCo;
half-day 4 ends with the end-to-end case study.

Typical session shape: 4 hours, with a 15-minute break about two hours in. Times in the guides are elapsed time from the start of the session.

## Contents of the `docs/` folder

| File | Use |
| --- | --- |
| [00-preparation.md](00-preparation.md) | D-7 / D-1 / Day-D checklist, accounts, Snowflake environment, budget |
| [01 … 04-half-day-N.md](01-half-day-1.md) | Timed schedule, key messages, step-by-step demos, trainer notes |
| [annexes/cheat-sheet.md](annexes/cheat-sheet.md) | One-page cheat sheet to hand out to participants |
| [annexes/evaluation.md](annexes/evaluation.md) | End-of-training quiz (with answers) and case study grading grid |
| [annexes/trainer-faq.md](annexes/trainer-faq.md) | Frequently asked questions and answers, common incidents |

The participant exercise sheets are in [`../exercises/`](../exercises), the solutions in [`../solutions/`](../solutions), and the slide decks in [`../slides/`](../slides).

## Working assumptions

- **Language**: English for all material; technical keywords (prompt, hook, skill…) are used as-is.
- **Audience**: mixed levels. The "🚀 Going further" blocks keep the fastest participants busy without slowing the group.
- **Environment**: each participant has a machine with a terminal, Python 3.10+, Git and a Claude account
  (Keyrus Team/Enterprise or an API — Application Programming Interface — key from the Claude Console).
  DuckDB replaces Snowflake if Snowflake access is not available: all exercises work without Snowflake.
- **Versions**: content checked against the Claude Code documentation of November 2026. Claude Code evolves quickly:
  re-run `claude --version` and skim the changelog the day before the session (see [00-preparation.md](00-preparation.md)).

## Key messages of the training (to repeat)

1. **An agent acts, it does not just answer**: it reads, runs, modifies. Hence the importance of permissions and review.
2. **Context is the scarce resource**: what goes into the context window determines quality *and* cost.
3. **Explore → plan → code → verify**: Plan Mode and tests are the two most cost-effective safeguards.
4. **Give Claude a way to check its own work** (tests, `dbt build`, expected result): it beats long explanations.
5. **The consultant remains responsible** for every line delivered to the client, whether written by them or by Claude.
