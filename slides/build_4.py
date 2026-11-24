# -*- coding: utf-8 -*-
# Half-day 4 deck, Keyrus template. Run: python slides/build_4.py
# STORYBOARD (# | section | message | layout | form | family)
#  1 cover | AI_Cover_Dark
#  2 agenda | Agenda_8_Items
#  3 S7 intercalaire Title_Slide_1
#  4 Claude handles Git like a dev | flow | blue
#  5 Four team rules | cards | blue
#  6 Three review levels | pyramid | blue
#  7 Reviews 1-2 prepare human review | versus | blue
#  8 CI/CD two workflows | versus | blue
#  9 claude.yml modes | flow | blue
# 10 Demo PR | flow | blue         11 Exercise 4.1 | flow | blue
# 12 7.2 What is shared | layers | blue   13 Collaborate | cards | blue
# 14 S8 intercalaire Title_Slide_2
# 15 context travels | flow | red   16 accounts | versus | red   17 Keyrus rule | versus | red
# 18 six risks | table | red   19 five AI risks | hub | red   20 safeguards | flow | red
# 21 cost | kpis | yellow   22 seven levers | table | yellow   23 compute | cards | yellow
# 24 demo usage | flow | yellow   25 break | custom | yellow
# 26 S9 intercalaire Title_Slide_3
# 27 requirement | kpis | yellow   28 two deliverables | hub | yellow
# 29 six milestones | timeline | yellow   30 business answers | cards | yellow
# 31 pitfalls | cards | yellow   32 presentations | flow | yellow   33 debrief | donut chart | yellow
# 34 recap | cards | blue   35 wrap-up | flow | blue   36 closing | cards | blue   37 thank you | closing
# Native-diagram content slides: 20 of 31
import sys
import os
SKILL = "C:/Users/Stefan.Duprey/.claude/plugins/synced/a8188927-62a2-4df9-9577-7c442b66f830_279e38b6-7f96-4e6c-900a-8904d25cb69d/keyrus-slides~g2/skills/keyrus-slides"
sys.path.insert(0, SKILL + "/scripts")
import kdeck
from diagrams import (add_flow, add_kpis, add_cards, add_timeline, add_layers, add_versus,
                      add_chart, add_pyramid, add_hub, custom, box, label)
from insert_table import add_table

prs = kdeck.new_deck()
T = "Title_Description_{}_Light"


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


def slide(fam, title, sub, note):
    s = kdeck.add(prs, T.format(fam.capitalize()), title=title, subtitle=sub)
    notes(s, note)
    return s


def section(layout, title, sub, note):
    s = kdeck.add(prs, layout, title=title)
    kdeck.fill(s, {20: sub})
    notes(s, note)
    return s


# 1 cover
s = kdeck.add(prs, "AI_Cover_Dark", title="Half-day 4: Delivery, Security, Costs & Case Study",
              subtitle="Claude Code for Data Consultants - Themes 7, 8 and 9")
notes(s, "Last session of the training. The session start time is up to the organiser; all timings are offsets from the start of the 4-hour session. Goal: leave with a PR reviewed and delivered, a security reflex, and one full end-to-end case behind you.")

# 2 agenda
s = kdeck.add(prs, "Agenda_8_Items", title="Agenda")
kdeck.fill(s, {16: "0:00 - 7.1 Git, reviews, CI/CD (30 min)", 17: "0:30 - Exercise 4.1: branch to PR (20 min)",
               18: "0:50 - 7.2 Reuse and collaboration (15 min)", 19: "1:05 - 8. Security, governance, costs (35 min)",
               20: "1:40 - Break (15 min)", 21: "1:55 - Exercise 4.2: case study, pairs (95 min)",
               22: "3:30 - Presentations and debrief (20 min)", 23: "3:50 - Quiz, survey, closing (10 min)"})
notes(s, "Timings are offsets from the start (0:00). Start time chosen by the organiser. The break stays a break. The case study is the longest block: protect it. Formats: 7.1 talk + demo; Exercise 4.1 hands-on; 7.2 talk; 8 talk + demo; Exercise 4.2 guided hands-on in pairs; presentations 3 pairs x 5 min plus debrief; quiz, survey and closing individual.")

# ===== Theme 7 (blue)
section("Title_Slide_1", "7. Industrialization and delivery", "Git, reviews, CI/CD and sharing what works  |  0:00 - 1:05",
        "Theme 7 covers 7.1 (30 min talk + demo), Exercise 4.1 (20 min) and 7.2 (15 min).")

s = slide("blue", "Claude handles Git like a developer", "Same discipline as a human, permissions as a safety net",
          "Claude runs git status, creates branches, commits, resolves conflicts and opens PRs through the gh CLI. The point of this block: the same discipline as for a human developer, with permissions as a safety net. One session per task, one branch per task.")
add_flow(s, [("Branch", "git checkout -b fix/..."), ("Commit", "Atomic, team format"), ("Pull request", "gh pr create"),
             ("CI + review", "CI first, then reviews"), ("Merge", "After human sign-off")],
         icons=["layers", "check-circle", "file-text", "shield-check", "rocket"], family="blue")

s = slide("blue", "Four team rules, already in settings.json", "Safe defaults for every mission",
          "Rules already in place in .claude/settings.json: git status/diff/log allowed without confirmation; git commit and git push set to ask. Commit message format is written in CLAUDE.md with one line of 'why'. Parallel work: git worktree add ../retailco-feature-x -b feature-x, one Claude Code session per worktree.")
add_cards(s, [("Safe by default", "status, diff, log allowed; commit and push ask"),
              ("One branch per task", "Never commit directly to main"),
              ("Team commit format", "In CLAUDE.md, with one line of why"),
              ("Small PRs", "One intent, reviewable in 10 minutes")],
          icons=["lock", "layers", "file-text", "check-circle"], family="blue")

s = slide("blue", "Three review levels, from fast to accountable", "The higher the level, the stronger the guarantee",
          "Level 1: /sql-review file.sql or 'review your diff' (fast, but the agent reviews its own work). Level 2: subagent data-reviewer (clean context, read-only, Sonnet), built-in /code-review and /security-review. Level 3: GitHub/GitLab PR, mandatory: the consultant signs off on what they deliver.")
add_pyramid(s, [("3. Human review", "The PR: the consultant signs off"),
                ("2. Independent review", "data-reviewer, /code-review, /security-review"),
                ("1. Guided self-review", "/sql-review, 'review your diff'")], family="blue")

s = slide("blue", "Reviews 1 and 2 prepare the human review", "Insist on this one: accountability stays human",
          "Insist on this one. AI reviews catch many problems, but accountability stays with the consultant.")
add_versus(s, ("AI reviews (levels 1-2)", ["Catch many problems", "Fast, clean context", "Prepare the human review"]),
           ("Human review (level 3)", ["Signs off what is delivered", "Never replaced", "The consultant is accountable"]),
           labels=("Prepare", "Decide"))

s = slide("blue", "CI/CD: two workflows, two different jobs", "Deterministic CI, Claude in the loop on the side",
          "ci.yml: classic CI (ruff, pytest, data generation, dbt build on DuckDB). Claude does not take part: CI must stay deterministic. claude.yml: official action anthropics/claude-code-action@v1. Setup: /install-github-app from Claude Code (installs the GitHub app, creates the secret, opens the workflow PR), or manually (Claude GitHub app + ANTHROPIC_API_KEY or CLAUDE_CODE_OAUTH_TOKEN secret + copy the workflow). On GitLab: equivalent CI/CD integration, see the Claude Code documentation 'GitLab CI/CD'.")
add_versus(s, ("ci.yml: deterministic", ["ruff, pytest, data generation", "dbt build on DuckDB", "Claude does not take part"]),
           ("claude.yml: Claude in the loop", ["claude-code-action@v1", "Interactive and automatic modes", "Setup: /install-github-app"]),
           labels=("CI", "Claude"))

s = slide("blue", "claude.yml: interactive and automatic modes", "Guardrails keep cost and scope bounded",
          "Interactive: a comment such as '@claude fix the failing dbt test' in a PR or issue triggers Claude. Automatic: on every PR, a review with a given instruction and a tool allowlist (--allowedTools), capped by --max-turns and a timeout-minutes. Guardrails keep cost and scope bounded.")
add_flow(s, [("Interactive", "@claude comment in a PR or issue"), ("Automatic", "Review on every PR, tool allowlist"),
             ("Guardrails", "--max-turns, timeout-minutes")],
         icons=["users", "settings", "lock"], family="blue")

s = slide("blue", "Demo: from a fix to a reviewed PR (10 min)", "DEMO - 10 min",
          "DEMO SCRIPT (10 min). 1) git checkout -b fix/fan-out-fct-orders; ask Claude to fix the fan-out with a test. 2) 'use the data-reviewer subagent to review my changes' -> read the verdict. 3) 'create the PR with gh, description in English: context, fix, quantified impact, tests'. 4) On GitHub: CI runs, the automatic review posts its comment; add an @claude in the PR to ask a question.")
add_flow(s, [("1. Fix on a branch", "fix/fan-out-fct-orders + test"), ("2. Independent review", "data-reviewer verdict"),
             ("3. Create the PR", "gh pr create: context, impact"), ("4. On GitHub", "CI, auto review, @claude")],
         icons=["settings", "user-check", "file-text", "cloud"], family="blue")

s = slide("blue", "Exercise 4.1: from branch to reviewed PR", "EXERCISE 4.1 - 20 min",
          "Each participant turns their Half-day 3 fixes into one clean PR: branch, atomic commits, data-reviewer review, generated then proofread PR description, green CI. Walk around; check that PR descriptions are proofread, not pasted. Exercise sheet: exercises/HD4_industrialization_case_study.md.")
add_flow(s, [("Clean history", "One fix per commit"), ("Review", "data-reviewer, /security-review"),
             ("Describe", "Claude drafts, you proofread"), ("Open the PR", "gh pr create, wait for CI")],
         icons=["layers", "user-check", "file-text", "rocket"], family="blue")

s = slide("blue", "7.2 What gets shared, and where it lives", "From the team repo to organization-wide rules",
          "Walk the layers top to bottom: from enforced organization rules, to Keyrus-wide plugin, to team-level files in the repository, to personal preferences. Instructions, permissions, hooks, skills, subagents: CLAUDE.md and .claude/ in the repo, shared with the project team via Git. Personal preferences: ~/.claude/, CLAUDE.local.md, settings.local.json, shared with nobody. Project MCP servers: .mcp.json (no secrets, environment variables only), project team. Keyrus know-how (dbt-model, SQL review, quality audit): internal plugin on a Git marketplace, all consultants. Enforced rules (prohibitions, allowed models): managed settings deployed by IT, the whole organization.")
add_layers(s, [("Organization: managed settings by IT", ["Prohibitions", "Allowed models"]),
               ("Keyrus plugin (Git marketplace)", ["dbt-model", "SQL review", "Quality audit"]),
               ("Project repo (shared via Git)", ["CLAUDE.md", ".claude/", ".mcp.json"]),
               ("Personal (shared with nobody)", ["~/.claude/", "CLAUDE.local.md", "settings.local"])],
           family="blue")

s = slide("blue", "Collaborate: capitalize what works", "Treat Claude assets like code",
          "Proposal to debate with the room: a Keyrus mission starter kit = a template repository with a standard CLAUDE.md, a secure .claude/settings.json, hooks, Data skills and the security checklist from theme 8. Each mission copies it, then enriches it with the client's business pitfalls.")
add_cards(s, [("CLAUDE.md as code", "Review it in PRs; a repeated correction becomes one line"),
              ("Document sessions", "/rename plus a PR summary: prompt, decisions, checks"),
              ("Capitalize", "A skill useful on 2 missions joins the Keyrus plugin"),
              ("Mission starter kit", "Template repo: CLAUDE.md, settings, hooks, skills. To discuss")],
          icons=["file-text", "users", "lightbulb", "rocket"], family="blue")

# ===== Theme 8 (red)
section("Title_Slide_2", "8. Security, governance and costs", "Client data, human oversight and consumption  |  1:05 - 1:40",
        "Theme 8: 8.1 client data confidentiality (15 min), 8.2 human oversight and AI risks (10 min), 8.3 optimizing consumption (10 min) including a 5 min demo.")

s = slide("red", "8.1 Everything in the context goes to the model", "Claude Code runs locally, but the context travels",
          "Claude Code runs locally, but everything that enters the context (prompts, content of files read, command outputs, including data rows if Claude runs a select *) is sent to the model, encrypted in transit (TLS 1.2+).")
add_flow(s, [("Your workstation", "Prompts, files read, command outputs"), ("Context", "Includes data rows if select *"),
             ("Model", "Sent encrypted (TLS 1.2+)")],
         icons=["users", "database", "brain"], family="red")

s = slide("red", "Commercial and consumer accounts are not the same", "Data usage, as documented in November 2026",
          "Source: Claude Code documentation, Data usage page, November 2026. ZDR = Zero Data Retention, possible on Claude for Enterprise after eligibility validation. Local transcripts live in ~/.claude/projects/ for 30 days (cleanupPeriodDays), in plain text, for both account types.")
add_versus(s, ("Team, Enterprise, API, cloud", ["No model training unless opted in", "30 days retention; ZDR on Enterprise", "Local transcripts: plain text, 30 days"]),
           ("Free, Pro, Max", ["Training depends on user setting", "30 days, or 5 years if training accepted", "Local transcripts: same"]),
           labels=("Commercial", "Consumer"))

s = slide("red", "Keyrus rule: commercial accounts only", "Never a personal account on client code or data",
          "State this clearly. Also check the client's contract: some clients require hosting in their own cloud (Bedrock, Google Cloud, Foundry), others prohibit any generative AI tool.")
add_versus(s, ("Commercial accounts only", ["For any client code or data", "Check the client contract first"]),
           ("Never a personal account", ["Some clients require their own cloud", "Others forbid generative AI tools"]),
           labels=("Allowed", "Forbidden"))

s = slide("red", "Six risks, six concrete measures on a mission", "What to put in place before the first prompt",
          "Secrets: deny on .env, dbt profiles, ~/.snowflake; vault. Personal data: anonymized or synthetic samples, 'aggregates only, 20 rows max', Snowflake dynamic masking. Destructive action: read-only role, blocking hooks, no production credentials on the workstation. Prompt injection: default mode on untrusted content, do not pipe untrusted content, curl/wget in deny, /sandbox. Telemetry: commercial accounts, CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 if the client requires it, no /feedback on client code. Local sessions: reduce cleanupPeriodDays, disk encryption.")
add_table(s, [["Risk", "Measure"],
              ["Reading secrets", "deny on .env, dbt profiles, ~/.snowflake; vault"],
              ["Personal data in context", "Anonymized samples; 20 rows max; masking"],
              ["Destructive action", "Read-only role; blocking hooks; no prod credentials"],
              ["Prompt injection", "default mode; curl/wget in deny; /sandbox"],
              ["Telemetry / feedback leak", "Commercial accounts; DISABLE_NONESSENTIAL_TRAFFIC=1"],
              ["Local copy of sessions", "Lower cleanupPeriodDays; disk encryption"]],
          top=2.0, font_size=12, header_size=12, height=3.9)

s = slide("red", "8.2 Five AI risks to name explicitly", "Naming them is the first safeguard",
          "Plausible but wrong code: the 4 bugs of Half-day 3 could have been written by an AI. Overconfidence: the better the tool, the less we review. Scope drift: the agent 'improves' files it was not asked to touch. Test circumvention: changing the test rather than the code. Dependence: a consultant who no longer understands the code they deliver.")
add_hub(s, "AI risks", [("Wrong code", "Plausible but wrong"), ("Overconfidence", "Less review"),
                        ("Scope drift", "Untouched files improved"), ("Test bypass", "Test changed, not code"),
                        ("Dependence", "Code not understood")],
        icons=["brain", "gauge", "layers", "lock", "users"], family="red")

s = slide("red", "Safeguards keep a human in control", "Five steps, from plan to signed PR",
          "Plan Mode before any non-trivial task; default or acceptEdits mode (no bypassPermissions outside a container); tests written or validated by a human; independent review; PR reviewed and signed off by a human; traceability (PR description mentions the use of Claude and the checks performed). For the enterprise: managed settings (enforced prohibitions, ability to disable bypassPermissions and auto mode), enterprise CLAUDE.md, usage tracking via OpenTelemetry, ConfigChange hooks to audit configuration changes.")
add_flow(s, [("Plan Mode", "Before any non-trivial task"), ("Safe mode", "No bypassPermissions outside a container"),
             ("Human tests", "Written or validated by a human"), ("Independent review", "Clean-context reviewer"),
             ("Signed PR", "Human sign-off, Claude use stated")],
         icons=["target", "lock", "check-circle", "user-check", "shield-check"], family="red")

s = slide("yellow", "8.3 What does Claude Code cost?", "Cost follows the volume of context processed",
          "Benchmarks from the Claude Code documentation, Manage costs page. Cost is proportional to the volume of context processed: every exchange resends the whole conversation. This is why the levers on the next slide are about context.")
add_kpis(s, [("$13", "per developer per active day", "on average"), ("$150-250", "per developer per month"),
             ("< $30", "per active day", "for 90% of users")], family="yellow")

s = slide("yellow", "Seven levers to control consumption", "Context first, then model, prompts and tools",
          "Context: /clear between tasks, /compact with instructions, CLAUDE.md under 200 lines, long procedures as skills. Model: Sonnet by default, Opus for architecture, Haiku for simple subagents (model: haiku), lower /effort. Prompts: specific rather than 'improve the repo'. Tools: CLI (gh, dbt, snow) rather than MCP when equivalent, disable unused MCP servers (/mcp), hooks filtering verbose output. Delegation: subagents for voluminous output. Method: Plan Mode, Esc early, small increments. Monitoring: /usage, /context, /insights; org side: spending limits and admin dashboards. Snowflake: dedicated XS warehouse, AUTO_SUSPEND = 60, resource monitor (snowflake/setup_training_env.sql).")
add_table(s, [["Lever", "Action"],
              ["Context", "/clear between tasks; /compact; CLAUDE.md under 200 lines; skills"],
              ["Model", "Sonnet by default; Opus for hard reasoning; Haiku for subagents"],
              ["Prompts", "Specific ('in auth.ts...'), not 'improve the repo'"],
              ["Tools", "CLI over MCP when equivalent; disable unused MCP servers"],
              ["Delegation", "Subagents for logs and tests: only the summary returns"],
              ["Method", "Plan Mode; Esc early; small increments"],
              ["Monitoring", "/usage, /context, /insights; org spending limits"]],
          top=2.0, font_size=12, header_size=12, height=4.2)

s = slide("yellow", "Do not forget the compute the agent triggers", "The Snowflake side has its own meter",
          "On the Snowflake side, the agent can trigger warehouse compute. See snowflake/setup_training_env.sql for the training setup: dedicated XS warehouse, AUTO_SUSPEND = 60, resource monitor.")
add_cards(s, [("Dedicated XS warehouse", "Agent queries stay on a small, isolated warehouse"),
              ("AUTO_SUSPEND = 60", "Stop paying after one idle minute"),
              ("Resource monitor", "A hard credit cap that suspends the warehouse")],
          icons=["database", "gauge", "lock"], family="yellow")

s = slide("yellow", "Demo: read your own usage (5 min)", "DEMO - 5 min",
          "DEMO SCRIPT (5 min). At the end of a demo session, run /usage then /context. Read with the room the breakdown (files read, MCP tools, CLAUDE.md) and the recommendations.")
add_flow(s, [("/usage", "Session cost, breakdown, recommendations"), ("/context", "Files read, MCP tools, CLAUDE.md"),
             ("Act on it", "Apply one lever from the table")],
         icons=["gauge", "chart-bar", "check-circle"], family="yellow")

s = slide("yellow", "Break: 15 minutes", "Back for the end-to-end case study, in pairs",
          "15 minutes. Break at 1:40, back at 1:55 for the case study. Use the time to check that pairs are formed and the environment (dbt, DuckDB, repo) works for everyone.")
with custom(s):
    box(s, 2.2, 2.6, 4.0, 1.6, "15 minutes", "Break", family="yellow", size=22)
    box(s, 7.1, 2.6, 4.0, 1.6, "Case study", "Back at 1:55, in pairs", family="blue", style="soft", size=18)
    label(s, 2.2, 4.8, 9.0, 0.5, "Check: pairs formed, dbt, DuckDB and repo working for everyone", size=14, bold=True, color="021E57")

# ===== Theme 9 (yellow)
section("Title_Slide_3", "9. End-to-end case study", "Churn-risk customers for RetailCo  |  1:55 - 3:50",
        "Theme 9: Exercise 4.2 (95 min, pairs), then presentations (20 min). Put the trainer in the 'business' role: answers are given only if asked.")

s = slide("yellow", "The requirement: customers at risk of churning", "Monthly, to trigger a retention campaign",
          "TO BE READ ALOUD. RetailCo's sales leadership wants to identify, every month, customers at risk of churning in order to trigger a retention campaign. A customer is 'at risk' if they have placed no non-cancelled order for more than 90 days (60 days for VIPs), while having placed at least 2 orders in the preceding 12 months. Deliverables: a dbt table the BI team can use, and a daily CSV export for the CRM (Customer Relationship Management) tool with no personal data in clear text.")
add_kpis(s, [("90 d", "without a non-cancelled order"), ("60 d", "threshold for VIP customers"),
             (">= 2", "orders in the preceding 12 months")], family="yellow")

s = slide("yellow", "Two deliverables, one rule: no personal data", "No name, no clear-text email in the CRM export",
          "The CRM export must not contain names or clear-text email. The key is a SHA-256 hash of the normalized email.")
add_hub(s, "At-risk customers", [("dbt table", "mart_customers_at_risk, for BI"), ("Python export", "export_at_risk.py, daily CSV"),
                                 ("Privacy rule", "Hashed customer key only")],
        icons=["database", "file-text", "lock"], family="yellow")

s = slide("yellow", "Exercise 4.2: six milestones in 95 minutes", "EXERCISE 4.2 - 95 min - pairs",
          "Indicative timings. Milestone 1 (10 min): questions to the 'business' (the trainer); assumptions written in docs/cas_pratique.md ('cas pratique' means case study; file name kept from the sample project): reference date, statuses retained, grain. Milestone 2 (15 min): Plan Mode; walk around the pairs and REFUSE a plan without tests or an explicit grain. Milestone 3 (25 min): dbt model + YAML, dbt build green (mart_customers_at_risk). Milestone 4 (20 min): Python export + pytest, pseudonymized email (export_at_risk.py). Milestone 5 (15 min): branch, data-reviewer review, PR with description, CI green. Milestone 6 (5 min): /usage readout and one CLAUDE.md improvement or skill proposal.")
add_timeline(s, [("10 min", "1. Scoping", "Questions, assumptions"), ("15 min", "2. Plan", "Plan Mode, validated"),
                 ("25 min", "3. dbt model", "Tested YAML, build green"), ("20 min", "4. Export", "pytest, hashed email"),
                 ("15 min", "5. Delivery", "Branch, review, PR, CI"), ("5 min", "6. Cost", "/usage, CLAUDE.md")],
             family="yellow")

s = slide("yellow", "Business answers: give them only when asked", "That is the point of milestone 1",
          "Give these answers only if the pairs ask: that is the point of milestone 1. Reference date: parameter as_of_date, default 2026-09-01 (data stops at the end of August 2026). Orders: statuses delivered, shipped, returned (not cancelled); future dates ignored. 12 months = the 365 days before as_of_date. Grain: one row per customer, ALL customers, with a boolean is_at_risk. Export: only at-risk customers, columns customer_key (SHA-256 of the normalized email), segment, days_since_last_order, orders_last_12m, revenue_last_12m; no name, no clear-text email.")
add_cards(s, [("Reference date", "as_of_date, default 2026-09-01; 12 months = 365 days"),
              ("Orders counted", "delivered, shipped, returned; future dates ignored"),
              ("Grain", "One row per customer, with boolean is_at_risk"),
              ("Export", "At-risk only: hashed key, segment, 3 metrics")],
          icons=["target", "check-circle", "layers", "file-text"], family="yellow")

s = slide("yellow", "Trainer view: frequent pitfalls to watch for", "Four traps that catch most pairs",
          "TRAINER NOTES. Frequent pitfalls: forgetting the VIP threshold; counting cancelled orders; using current_date (non-reproducible); joining the uncorrected fct_orders (fan-out); exporting the email in clear text 'just to test'; hashing without normalization (case, spaces); future dates yielding a negative days_since_last_order. If a pair finishes early: make the model incremental, or add a scheduled GitHub Action that produces the export. Evaluation grid: docs/annexes/evaluation.md. Solutions: solutions/dbt_project/models/marts/mart_customers_at_risk.sql and solutions/src/retail_pipeline/export_at_risk.py.")
add_cards(s, [("Thresholds", "VIP 60 days; cancelled orders excluded"),
              ("Reproducibility", "as_of_date, not current_date; ignore future dates"),
              ("Joins", "Uncorrected fct_orders causes a fan-out"),
              ("Privacy", "Normalize the email before hashing; never clear text")],
          icons=["gauge", "settings", "network", "lock"], family="yellow")

s = slide("yellow", "Presentations: 3 pairs, 5 minutes each", "PRESENTATIONS - 20 min",
          "Three pairs, 5 minutes each. Debrief: compare the definitions chosen. Differences in figures almost always come from different assumptions, not bugs. REFERENCE RESULT (solution, as_of_date = 2026-09-01): 665 at-risk customers out of 2,000 (291 VIP, 202 B2B, 172 B2C); 641 exported, 24 excluded for lack of an email. A gap of a few dozen usually comes from a different assumption (statuses, 365-day boundary).")
add_flow(s, [("Initial plan", "Decided before coding"), ("What worked", "What Claude did well"),
             ("Corrections", "What you had to fix"), ("Session cost", "Readout from /usage")],
         icons=["target", "check-circle", "settings", "gauge"], family="yellow")

s = slide("yellow", "Debrief: different numbers, different assumptions", "665 at-risk customers out of 2,000 in the reference solution",
          "Reference result (solution, as_of_date = 2026-09-01): 665 at-risk customers out of 2,000 (291 VIP, 202 B2B, 172 B2C); 641 exported, 24 excluded for lack of an email. A gap of a few dozen usually comes from a different assumption (statuses, 365-day boundary). Do not share these figures before the pairs have presented.")
add_chart(s, "donut", ["VIP", "B2B", "B2C"], [("At-risk customers", [291, 202, 172])], family="yellow")

# ===== Recap (blue)
s = slide("blue", "Half-day 4 in four messages", "What to remember from this session",
          "Recap of the half-day before the training-wide wrap-up.")
add_cards(s, [("Reviews prepare", "AI reviews prepare the human review; you sign off"),
              ("Share what works", "CLAUDE.md, skills, plugin: capitalize across missions"),
              ("Protect client data", "Commercial accounts, deny rules, samples, sandbox"),
              ("Control the cost", "Manage context, right model, measure with /usage")],
          icons=["user-check", "users", "shield-check", "gauge"], family="blue")

s = slide("blue", "Training wrap-up: from first prompt to delivered PR", "A workflow, not just a tool: plan, build, verify, review, deliver",
          "Training-wide wrap-up. Walk through the four half-days: Fundamentals, Prompting & Context; Code Exploration & Data Development; Testing, Quality & Integrations; Delivery, Security, Costs & Case Study. Congratulate the group, then move to the quiz and survey. You now have a workflow, not just a tool: plan, build, verify, review, deliver.")
add_flow(s, [("Half-day 1", "Fundamentals, Prompting & Context"), ("Half-day 2", "Code Exploration & Data Development"),
             ("Half-day 3", "Testing, Quality & Integrations"), ("Half-day 4", "Delivery, Security, Costs & Case Study")],
         icons=["rocket", "database", "check-circle", "shield-check"], family="blue")

s = slide("blue", "Closing: quiz, survey and take-aways", "CLOSING - 10 min - individual",
          "10-question quiz (docs/annexes/evaluation.md); feedback survey; hand over the cheat sheet (docs/annexes/aide-memoire.md) and repository access (solutions branch open to everyone). 10 minutes, individual.")
add_cards(s, [("10-question quiz", "Individual, from the evaluation annex"),
              ("Feedback survey", "Tell us what to keep and what to change"),
              ("Cheat sheet and repo", "The solutions branch is open to everyone")],
          icons=["file-text", "users", "rocket"], family="blue")

s = kdeck.add_closing(prs, title="Thank you", subtitle="Questions, feedback and your next mission: put Claude Code to work")
notes(s, "Closing slide. Stay available for questions after the survey.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "4-delivery-security-costs-case-study.pptx")
kdeck.save(prs, out)
print("wrote", out)
