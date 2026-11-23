// Generator for the half-day 4 deck. Run from slides/: node 4-delivery-security-costs-case-study.js
const { THEME, newDeck, contentSlide, darkSlide, cards, stats } = require("./theme");
const { pres } = newDeck("Half-day 4: Industrialize, secure, deliver");
const K = THEME.colors;
const SH = pres.ShapeType;

// --- local helpers (kept here so theme.js stays untouched) ---
function tag(s, text, color = K.accent3) {
  s.addText(text, { x: 0.6, y: 1.3, w: 4.6, h: 0.45, shape: SH.roundRect, rectRadius: 0.1, fill: { color }, color: "FFFFFF", bold: true, fontSize: 14, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
// horizontal process flow: [{head, body}] with arrows between boxes
function flow(s, steps, y = 2.2, h = 3.2) {
  const gap = 0.45, w = (12.1 - gap * (steps.length - 1)) / steps.length;
  steps.forEach((st, i) => {
    const x = 0.6 + i * (w + gap);
    s.addShape(SH.roundRect, { x, y, w, h, fill: { color: K.lt2 }, line: { color: K.lt2 }, rectRadius: 0.1 });
    s.addText(st.head, { x: x + 0.2, y: y + 0.2, w: w - 0.4, h: 0.8, fontSize: 18, bold: true, color: K.dk2, margin: 0, valign: "top", isTextBox: true });
    if (st.body) s.addText(st.body, { x: x + 0.2, y: y + 1.05, w: w - 0.4, h: h - 1.25, fontSize: 14, color: K.dk1, margin: 0, valign: "top", isTextBox: true });
    if (i < steps.length - 1) s.addShape(SH.line, { x: x + w + 0.05, y: y + h / 2, w: gap - 0.1, h: 0, line: { color: K.accent2, width: 3, endArrowType: "triangle" } });
  });
}
// big one-sentence message on a tinted panel
function statement(s, text, sub, y = 1.9) {
  s.addShape(SH.roundRect, { x: 0.6, y, w: 12.1, h: 3.2, fill: { color: K.lt2 }, line: { color: K.lt2 }, rectRadius: 0.1 });
  s.addText(text, { x: 1.0, y: y + 0.3, w: 11.3, h: 1.7, fontSize: 30, bold: true, color: K.dk2, margin: 0, valign: "middle", isTextBox: true });
  if (sub) s.addText(sub, { x: 1.0, y: y + 2.1, w: 11.3, h: 0.9, fontSize: 18, color: K.dk1, margin: 0, valign: "top", isTextBox: true });
}
function table(s, head, rows, colW, y = 1.6, fs = 14, rowH = 0.5) {
  const hdr = head.map(t => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: K.dk2 }, fontSize: fs, align: "left", valign: "middle" } }));
  const body = rows.map(r => r.map((t, j) => ({ text: t, options: { fontSize: fs, color: K.dk1, align: "left", valign: "middle", bold: j === 0, fill: { color: "FFFFFF" } } })));
  s.addTable([hdr, ...body], { x: 0.6, y, w: 12.1, colW, rowH, border: { type: "solid", pt: 0.75, color: "CBD5E1" }, margin: [0.05, 0.1, 0.05, 0.1], fontFace: "Calibri" });
}
function footerNote(s, text) {
  s.addText(text, { x: 0.6, y: 6.3, w: 12.1, h: 0.5, fontSize: 14, italic: true, color: "475569", margin: 0, valign: "top", isTextBox: true });
}

// ================= Title + agenda =================
let s = darkSlide(pres, "Half-day 4: Industrialize, secure, deliver", "Claude Code for Data Consultants  |  Themes 7, 8 and 9",
  "Last session of the training. The session start time is up to the organiser (e.g. 09:00 or 13:30); all timings are offsets from the start of the 4-hour session. Goal: leave with a PR reviewed and delivered, a security reflex, and one full end-to-end case behind you.");

s = contentSlide(pres, "Agenda: 4 hours, from theory to a delivered case",
  "Timings are offsets from the start (0:00). Start time chosen by the organiser. The break stays a break. The case study is the longest block: protect it.");
table(s, ["Offset", "Duration", "Sequence", "Format"], [
  ["0:00", "30 min", "7.1 Git, code reviews and CI/CD", "Talk + demo"],
  ["0:30", "20 min", "Exercise 4.1: from branch to reviewed PR", "Hands-on"],
  ["0:50", "15 min", "7.2 Reusability and collaboration", "Talk"],
  ["1:05", "35 min", "8. Security, governance, costs", "Talk + demo"],
  ["1:40", "15 min", "Break", ""],
  ["1:55", "95 min", "Exercise 4.2: end-to-end case study (pairs)", "Guided hands-on"],
  ["3:30", "20 min", "Presentations (3 pairs x 5 min) + debrief", "Discussion"],
  ["3:50", "10 min", "Quiz, feedback survey, closing", "Individual"],
], [1.4, 1.6, 6.7, 2.4], 1.6, 14, 0.52);

// ================= Theme 7 =================
darkSlide(pres, "7. Industrialization and delivery", "Git, reviews, CI/CD and sharing what works  |  0:00 - 1:05",
  "Theme 7 covers 7.1 (30 min talk + demo), Exercise 4.1 (20 min) and 7.2 (15 min).");

s = contentSlide(pres, "Claude handles Git like a developer",
  "Claude runs git status, creates branches, commits, resolves conflicts and opens PRs through the gh CLI. The point of this block: the same discipline as for a human developer, with permissions as a safety net.");
flow(s, [
  { head: "Branch", body: "git checkout -b fix/..." },
  { head: "Commit", body: "Atomic commits, team message format" },
  { head: "Pull request", body: "gh pr create, described by Claude" },
  { head: "CI + review", body: "Deterministic CI, then reviews" },
  { head: "Merge", body: "After human sign-off" },
], 2.0, 3.0);
footerNote(s, "One session per task, one branch per task.");

s = contentSlide(pres, "Four team rules, already in .claude/settings.json",
  "Rules already in place in .claude/settings.json: git status/diff/log allowed without confirmation; git commit and git push set to ask. Commit message format is written in CLAUDE.md with one line of 'why'. Parallel work: git worktree add ../retailco-feature-x -b feature-x, one Claude Code session per worktree.");
cards(pres, s, [
  { head: "Safe by default", body: "status, diff, log allowed. commit and push set to ask." },
  { head: "One branch per task", body: "Never commit directly to main." },
  { head: "Team commit format", body: "Written in CLAUDE.md, with one line of why." },
  { head: "Small PRs", body: "One PR = one intent, reviewable in 10 minutes." },
], 1.7, 3.8);
footerNote(s, "Working in parallel: Git worktrees, one Claude Code session per worktree.");

s = contentSlide(pres, "Three review levels, from fast to accountable",
  "Level 1: /sql-review file.sql or 'review your diff' (fast, but the agent reviews its own work). Level 2: subagent data-reviewer (clean context, read-only, Sonnet), built-in /code-review and /security-review. Level 3: GitHub/GitLab PR, mandatory: the consultant signs off on what they deliver.");
cards(pres, s, [
  { head: "Guided self-review", body: "/sql-review, or ask 'review your diff'. Fast, but the agent reviews its own work." },
  { head: "Independent review", body: "data-reviewer subagent, /code-review, /security-review. Fresh eyes, clean context, read-only." },
  { head: "Human review", body: "The PR. Mandatory: the consultant signs off on what they deliver." },
], 1.7, 4.3);

s = contentSlide(pres, "Key message: reviews 1 and 2 prepare the human review",
  "Insist on this one. AI reviews catch many problems, but accountability stays with the consultant.");
statement(s, "Levels 1 and 2 prepare the human review. They never replace it.", "The consultant signs off on what they deliver.");

s = contentSlide(pres, "CI/CD: two workflows with two different jobs",
  "ci.yml: classic CI (ruff, pytest, data generation, dbt build on DuckDB). Claude does not take part: CI must stay deterministic. claude.yml: official action anthropics/claude-code-action@v1. Setup: /install-github-app from Claude Code (installs the GitHub app, creates the secret, opens the workflow PR), or manually (Claude GitHub app + ANTHROPIC_API_KEY or CLAUDE_CODE_OAUTH_TOKEN secret + copy the workflow). On GitLab: equivalent CI/CD integration, see the Claude Code documentation 'GitLab CI/CD'.");
cards(pres, s, [
  { head: "ci.yml: deterministic", body: "ruff, pytest, data generation, dbt build on DuckDB. Claude does not take part: CI must stay deterministic." },
  { head: "claude.yml: Claude in the loop", body: "Official action anthropics/claude-code-action@v1. Interactive and automatic modes." },
], 1.7, 3.6);
footerNote(s, "Setup: /install-github-app from Claude Code, or manually (GitHub app + secret + workflow). GitLab has an equivalent integration.");

s = contentSlide(pres, "claude.yml: interactive and automatic modes",
  "Interactive: a comment such as '@claude fix the failing dbt test' in a PR or issue triggers Claude. Automatic: on every PR, a review with a given instruction and a tool allowlist (--allowedTools), capped by --max-turns and a timeout-minutes. Guardrails keep cost and scope bounded.");
flow(s, [
  { head: "Interactive", body: "A comment such as '@claude fix the failing dbt test' in a PR or issue triggers Claude." },
  { head: "Automatic", body: "On every PR: a review with a fixed instruction and a tool allowlist (--allowedTools)." },
  { head: "Guardrails", body: "Capped by --max-turns and timeout-minutes." },
], 1.9, 3.6);

s = contentSlide(pres, "Demo: from a fix to a reviewed PR (10 min)",
  "DEMO SCRIPT (10 min). 1) git checkout -b fix/fan-out-fct-orders; ask Claude to fix the fan-out with a test. 2) 'use the data-reviewer subagent to review my changes' -> read the verdict. 3) 'create the PR with gh, description in English: context, fix, quantified impact, tests'. 4) On GitHub: CI runs, the automatic review posts its comment; add an @claude in the PR to ask a question.");
tag(s, "DEMO  |  10 min");
flow(s, [
  { head: "1. Fix on a branch", body: "fix/fan-out-fct-orders, with a test" },
  { head: "2. Independent review", body: "data-reviewer subagent gives a verdict" },
  { head: "3. Create the PR", body: "gh pr create: context, fix, impact, tests" },
  { head: "4. On GitHub", body: "CI runs, auto review comments, @claude for questions" },
], 2.1, 3.4);

s = contentSlide(pres, "Exercise 4.1: from branch to reviewed PR",
  "Each participant turns their Half-day 3 fixes into one clean PR: branch, atomic commits, data-reviewer review, generated then proofread PR description, green CI. Walk around; check that PR descriptions are proofread, not pasted. Exercise sheet: exercises/HD4_industrialization_case_study.md.");
tag(s, "EXERCISE 4.1  |  20 min");
flow(s, [
  { head: "Clean history", body: "One fix per commit, type(scope): message" },
  { head: "Review", body: "data-reviewer subagent and /security-review" },
  { head: "Describe", body: "Claude drafts the PR text, you proofread it" },
  { head: "Open the PR", body: "gh pr create, wait for CI, reply with @claude" },
], 2.1, 3.4);

s = contentSlide(pres, "7.2 What gets shared, and where it lives",
  "Walk the table top to bottom: from team-level files in the repository, to personal preferences, to Keyrus-wide plugin, to enforced organization rules. MCP config uses environment variables, never secrets.");
table(s, ["What", "Where", "Shared with"], [
  ["Instructions, permissions, hooks, skills, subagents", "CLAUDE.md, .claude/ in the repo", "Project team (via Git)"],
  ["Personal preferences", "~/.claude/, CLAUDE.local.md, settings.local.json", "Nobody"],
  ["Project MCP servers", ".mcp.json (no secrets)", "Project team"],
  ["Keyrus know-how (dbt-model, SQL review, quality audit)", "Internal plugin on a Git marketplace", "All consultants"],
  ["Enforced rules (prohibitions, allowed models)", "Managed settings deployed by IT", "The whole organization"],
], [4.6, 4.6, 2.9], 1.7, 14, 0.75);

s = contentSlide(pres, "Collaborate: capitalize what works",
  "Proposal to debate with the room: a Keyrus mission starter kit = a template repository with a standard CLAUDE.md, a secure .claude/settings.json, hooks, Data skills and the security checklist from theme 8. Each mission copies it, then enriches it with the client's business pitfalls.");
cards(pres, s, [
  { head: "Treat CLAUDE.md as code", body: "Review it in PRs. A correction made to Claude twice becomes one line in CLAUDE.md." },
  { head: "Document sessions", body: "/rename plus a PR summary: prompt, decisions, checks." },
  { head: "Capitalize", body: "A skill that proved useful on 2 missions moves into the Keyrus plugin." },
  { head: "Mission starter kit", body: "Template repo: CLAUDE.md, secure settings, hooks, Data skills, checklist. To discuss." },
], 1.7, 4.0);

// ================= Theme 8 =================
darkSlide(pres, "8. Security, governance and costs", "Client data, human oversight and consumption  |  1:05 - 1:40",
  "Theme 8: 8.1 client data confidentiality (15 min), 8.2 human oversight and AI risks (10 min), 8.3 optimizing consumption (10 min) including a 5 min demo.");

s = contentSlide(pres, "8.1 Everything in the context goes to the model",
  "Claude Code runs locally, but everything that enters the context (prompts, content of files read, command outputs, including data rows if Claude runs a select *) is sent to the model, encrypted in transit (TLS 1.2+).");
flow(s, [
  { head: "Your workstation", body: "Prompts, files read, command outputs" },
  { head: "Context", body: "Includes data rows if Claude runs select *" },
  { head: "Model", body: "Sent encrypted in transit (TLS 1.2+)" },
], 1.9, 3.0);
footerNote(s, "Claude Code runs locally, but the context is what travels.");

s = contentSlide(pres, "Commercial and consumer accounts are not the same",
  "Source: Claude Code documentation, Data usage page, November 2026. ZDR = Zero Data Retention, possible on Claude for Enterprise after eligibility validation. Local transcripts live in ~/.claude/projects/ for 30 days (cleanupPeriodDays), in plain text, for both account types.");
table(s, ["", "Commercial (Team, Enterprise, API, cloud)", "Consumer (Free, Pro, Max)"], [
  ["Model training", "No, unless voluntarily opted in", "Depends on the user's setting"],
  ["Retention", "30 days; ZDR possible on Enterprise", "30 days, or 5 years if training use accepted"],
  ["Locally", "Plain-text transcripts, 30 days", "Same"],
], [2.4, 5.0, 4.7], 1.7, 16, 0.85);
footerNote(s, "Locally: ~/.claude/projects/, cleanupPeriodDays. Source: Claude Code documentation, Data usage, November 2026.");

s = contentSlide(pres, "Keyrus rule: commercial accounts only",
  "State this clearly. Also check the client's contract: some clients require hosting in their own cloud (Bedrock, Google Cloud, Foundry), others prohibit any generative AI tool.");
statement(s, "Commercial accounts only for client code or data. Never a personal account.", "Check the client contract: some require their own cloud (Bedrock, Google Cloud, Foundry); others forbid generative AI tools.");

s = contentSlide(pres, "Six risks, six concrete measures on a mission",
  "Secrets: deny on .env, dbt profiles, ~/.snowflake; vault. Personal data: anonymized or synthetic samples, 'aggregates only, 20 rows max', Snowflake dynamic masking. Destructive action: read-only role, blocking hooks, no production credentials on the workstation. Prompt injection: default mode on untrusted content, do not pipe untrusted content, curl/wget in deny, /sandbox. Telemetry: commercial accounts, CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 if the client requires it, no /feedback on client code. Local sessions: reduce cleanupPeriodDays, disk encryption.");
table(s, ["Risk", "Measure"], [
  ["Reading secrets", "deny on .env, dbt profiles, ~/.snowflake; secrets in a vault"],
  ["Personal data in context", "Anonymized samples; 'aggregates only, 20 rows max'; masking"],
  ["Destructive action", "Read-only role; blocking hooks; no production credentials"],
  ["Prompt injection", "default mode; curl/wget in deny; /sandbox"],
  ["Telemetry / feedback leak", "Commercial accounts; CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1"],
  ["Local copy of sessions", "Lower cleanupPeriodDays; disk encryption"],
], [3.4, 8.7], 1.6, 14, 0.65);

s = contentSlide(pres, "8.2 Five AI risks to name explicitly",
  "Plausible but wrong code: the 4 bugs of Half-day 3 could have been written by an AI. Overconfidence: the better the tool, the less we review. Scope drift: the agent 'improves' files it was not asked to touch. Test circumvention: changing the test rather than the code. Dependence: a consultant who no longer understands the code they deliver.");
cards(pres, s, [
  { head: "Wrong code", body: "Plausible but wrong. The HD3 bugs could be AI-written." },
  { head: "Overconfidence", body: "The better the tool, the less we review." },
  { head: "Scope drift", body: "Files nobody asked to touch get improved." },
  { head: "Test bypass", body: "Changing the test, not the code." },
  { head: "Dependence", body: "Delivering code you no longer understand." },
], 1.7, 4.0);

s = contentSlide(pres, "Safeguards keep a human in control",
  "Plan Mode before any non-trivial task; default or acceptEdits mode (no bypassPermissions outside a container); tests written or validated by a human; independent review; PR reviewed and signed off by a human; traceability (PR description mentions the use of Claude and the checks performed). For the enterprise: managed settings (enforced prohibitions, ability to disable bypassPermissions and auto mode), enterprise CLAUDE.md, usage tracking via OpenTelemetry, ConfigChange hooks to audit configuration changes.");
flow(s, [
  { head: "Plan Mode", body: "Before any non-trivial task" },
  { head: "Safe mode", body: "default or acceptEdits; no bypassPermissions outside a container" },
  { head: "Human tests", body: "Written or validated by a human" },
  { head: "Independent review", body: "Clean-context reviewer" },
  { head: "Signed PR", body: "Human sign-off, mentions Claude usage" },
], 1.9, 3.4);
footerNote(s, "Enterprise level: managed settings, enterprise CLAUDE.md, OpenTelemetry usage tracking, ConfigChange hooks.");

s = contentSlide(pres, "8.3 What does Claude Code cost?",
  "Benchmarks from the Claude Code documentation, Manage costs page. Cost is proportional to the volume of context processed: every exchange resends the whole conversation. This is why the levers on the next slide are about context.");
stats(pres, s, [
  { value: "$13", label: "per developer per active day, on average" },
  { value: "$150-250", label: "per developer per month" },
  { value: "< $30", label: "per active day for 90% of users" },
], 1.9);
footerNote(s, "Cost follows the volume of context processed: every exchange resends the whole conversation.");

s = contentSlide(pres, "Seven levers to control consumption",
  "Context: /clear between tasks, /compact with instructions, CLAUDE.md under 200 lines, long procedures as skills. Model: Sonnet by default, Opus for architecture, Haiku for simple subagents (model: haiku), lower /effort. Prompts: specific rather than 'improve the repo'. Tools: CLI (gh, dbt, snow) rather than MCP when equivalent, disable unused MCP servers (/mcp), hooks filtering verbose output. Delegation: subagents for voluminous output. Method: Plan Mode, Esc early, small increments. Monitoring: /usage, /context, /insights; org side: spending limits and admin dashboards. Snowflake: dedicated XS warehouse, AUTO_SUSPEND = 60, resource monitor (snowflake/setup_training_env.sql).");
table(s, ["Lever", "Action"], [
  ["Context", "/clear between tasks; /compact; CLAUDE.md under 200 lines; skills for long procedures"],
  ["Model", "Sonnet by default; Opus for hard reasoning; Haiku for simple subagents; lower /effort"],
  ["Prompts", "Specific ('in auth.ts...'), not 'improve the repo'"],
  ["Tools", "CLI over MCP when equivalent; disable unused MCP servers; filter verbose output"],
  ["Delegation", "Subagents for logs and tests: only the summary comes back"],
  ["Method", "Plan Mode; Esc early; small increments"],
  ["Monitoring", "/usage, /context, /insights; org spending limits"],
], [2.2, 9.9], 1.5, 14, 0.62);

s = contentSlide(pres, "Do not forget the compute the agent triggers",
  "On the Snowflake side, the agent can trigger warehouse compute. See snowflake/setup_training_env.sql for the training setup: dedicated XS warehouse, AUTO_SUSPEND = 60, resource monitor.");
cards(pres, s, [
  { head: "Dedicated XS warehouse", body: "Keep agent queries on a small, isolated warehouse." },
  { head: "AUTO_SUSPEND = 60", body: "Stop paying after one idle minute." },
  { head: "Resource monitor", body: "A hard credit cap that suspends the warehouse." },
], 1.7, 3.6);
footerNote(s, "Reference: snowflake/setup_training_env.sql");

s = contentSlide(pres, "Demo: read your own usage (5 min)",
  "DEMO SCRIPT (5 min). At the end of a demo session, run /usage then /context. Read with the room the breakdown (files read, MCP tools, CLAUDE.md) and the recommendations.");
tag(s, "DEMO  |  5 min");
flow(s, [
  { head: "/usage", body: "Session cost, breakdown by skill, subagent and MCP, recommendations" },
  { head: "/context", body: "What fills the context: files read, MCP tools, CLAUDE.md" },
  { head: "Act on it", body: "Pick one lever from the previous slide and apply it" },
], 2.1, 3.4);

s = contentSlide(pres, "Break", "15 minutes. Break at 1:40, back at 1:55 for the case study. Use the time to check that pairs are formed and the environment (dbt, DuckDB, repo) works for everyone.");
statement(s, "15 minutes", "Back at 1:55 for the end-to-end case study, in pairs.");

// ================= Theme 9 =================
darkSlide(pres, "9. End-to-end case study", "Churn-risk customers for RetailCo  |  1:55 - 3:50",
  "Theme 9: Exercise 4.2 (95 min, pairs), then presentations (20 min). Put the trainer in the 'business' role: answers are given only if asked.");

s = contentSlide(pres, "The requirement: customers at risk of churning",
  "TO BE READ ALOUD. RetailCo's sales leadership wants to identify, every month, customers at risk of churning in order to trigger a retention campaign. A customer is 'at risk' if they have placed no non-cancelled order for more than 90 days (60 days for VIPs), while having placed at least 2 orders in the preceding 12 months. Deliverables: a dbt table the BI team can use, and a daily CSV export for the CRM (Customer Relationship Management) tool with no personal data in clear text.");
stats(pres, s, [
  { value: "90 d", label: "without a non-cancelled order" },
  { value: "60 d", label: "threshold for VIP customers" },
  { value: ">= 2", label: "orders in the preceding 12 months" },
], 1.7);
footerNote(s, "Deliverables: a dbt table for the BI team, and a daily CSV export for the CRM with no personal data in clear text.");

s = contentSlide(pres, "Two deliverables, one rule: no personal data in clear text",
  "The CRM export must not contain names or clear-text email. The key is a SHA-256 hash of the normalized email.");
flow(s, [
  { head: "dbt table", body: "marts/mart_customers_at_risk.sql, documented and tested, for the BI team" },
  { head: "Python export", body: "export_at_risk.py: daily CSV for the CRM, pytest tests" },
  { head: "Privacy rule", body: "No name, no clear-text email. Hashed customer key only." },
], 1.9, 3.4);

s = contentSlide(pres, "Exercise 4.2: six milestones in 95 minutes",
  "Indicative timings. Milestone 1: questions to the 'business' (the trainer); assumptions written in docs/cas_pratique.md ('cas pratique' means case study; file name kept from the sample project): reference date, statuses retained, grain. Milestone 2: Plan Mode; walk around the pairs and REFUSE a plan without tests or an explicit grain. Milestone 3: dbt model + YAML, dbt build green. Milestone 4: Python export + pytest, pseudonymized email. Milestone 5: branch, data-reviewer review, PR with description, CI green. Milestone 6: /usage readout and one CLAUDE.md improvement or skill proposal.");
tag(s, "EXERCISE 4.2  |  95 min  |  pairs");
table(s, ["#", "Milestone", "Time", "Expected"], [
  ["1", "Scoping", "10 min", "Questions to the business; assumptions written down"],
  ["2", "Exploration and plan", "15 min", "Plan Mode; plan validated by the trainer"],
  ["3", "dbt model", "25 min", "mart_customers_at_risk + tested YAML; dbt build green"],
  ["4", "Python export", "20 min", "export_at_risk.py + pytest; hashed email"],
  ["5", "Delivery", "15 min", "Branch, review, PR, CI green"],
  ["6", "Cost review", "5 min", "/usage readout; one CLAUDE.md improvement"],
], [0.6, 3.0, 1.4, 7.1], 1.9, 14, 0.58);

s = contentSlide(pres, "Business answers: give them only when asked",
  "Give these answers only if the pairs ask: that is the point of milestone 1. Reference date: parameter as_of_date, default 2026-09-01 (data stops at the end of August 2026). Orders: statuses delivered, shipped, returned (not cancelled); future dates ignored. 12 months = the 365 days before as_of_date. Grain: one row per customer, ALL customers, with a boolean is_at_risk. Export: only at-risk customers, columns customer_key (SHA-256 of the normalized email), segment, days_since_last_order, orders_last_12m, revenue_last_12m; no name, no clear-text email.");
cards(pres, s, [
  { head: "Reference date", body: "as_of_date, default 2026-09-01. 12 months = 365 days before." },
  { head: "Orders counted", body: "delivered, shipped, returned. Not cancelled. Future dates ignored." },
  { head: "Grain", body: "One row per customer, all customers, with boolean is_at_risk." },
  { head: "Export", body: "At-risk only: customer_key (SHA-256 of normalized email), segment, 3 metrics." },
], 1.7, 4.4);

s = contentSlide(pres, "Trainer view: frequent pitfalls to watch for",
  "TRAINER NOTES. Frequent pitfalls: forgetting the VIP threshold; counting cancelled orders; using current_date (non-reproducible); joining the uncorrected fct_orders (fan-out); exporting the email in clear text 'just to test'; hashing without normalization (case, spaces); future dates yielding a negative days_since_last_order. If a pair finishes early: make the model incremental, or add a scheduled GitHub Action that produces the export. Evaluation grid: docs/annexes/evaluation.md. Solutions: solutions/dbt_project/models/marts/mart_customers_at_risk.sql and solutions/src/retail_pipeline/export_at_risk.py.");
cards(pres, s, [
  { head: "Thresholds", body: "VIP 60 days; cancelled orders excluded." },
  { head: "Reproducibility", body: "No current_date: use as_of_date. Ignore future dates." },
  { head: "Joins", body: "Uncorrected fct_orders causes a fan-out." },
  { head: "Privacy", body: "Normalize the email (case, spaces) before hashing. Never export clear text." },
], 1.7, 4.0);

s = contentSlide(pres, "Presentations: 3 pairs, 5 minutes each",
  "Three pairs, 5 minutes each. Debrief: compare the definitions chosen. Differences in figures almost always come from different assumptions, not bugs. REFERENCE RESULT (solution, as_of_date = 2026-09-01): 665 at-risk customers out of 2,000 (291 VIP, 202 B2B, 172 B2C); 641 exported, 24 excluded for lack of an email. A gap of a few dozen usually comes from a different assumption (statuses, 365-day boundary).");
tag(s, "PRESENTATIONS  |  20 min", K.accent4);
flow(s, [
  { head: "Initial plan", body: "What you decided before coding" },
  { head: "What worked", body: "What Claude did well" },
  { head: "Corrections", body: "What you had to fix" },
  { head: "Session cost", body: "Readout from /usage" },
], 2.1, 3.0);

s = contentSlide(pres, "Debrief: different numbers mean different assumptions",
  "Reference result (solution, as_of_date = 2026-09-01): 665 at-risk customers out of 2,000 (291 VIP, 202 B2B, 172 B2C); 641 exported, 24 excluded for lack of an email. A gap of a few dozen usually comes from a different assumption (statuses, 365-day boundary). Do not share these figures before the pairs have presented.");
stats(pres, s, [
  { value: "665", label: "at-risk customers out of 2,000 in the reference solution" },
  { value: "641", label: "exported; 24 excluded for lack of an email" },
  { value: "291", label: "VIP at-risk (202 B2B, 172 B2C)" },
], 1.7);
footerNote(s, "Reference solution with as_of_date = 2026-09-01. A gap of a few dozen: look at statuses and the 365-day boundary first.");

// ================= Recap + closing =================
s = contentSlide(pres, "Half-day 4 in four messages",
  "Recap of the half-day before the training-wide wrap-up.");
cards(pres, s, [
  { head: "Reviews prepare", body: "AI reviews prepare the human review; the consultant signs off." },
  { head: "Share what works", body: "CLAUDE.md, skills, plugin: capitalize across missions." },
  { head: "Protect client data", body: "Commercial accounts, deny rules, samples, sandbox." },
  { head: "Control the cost", body: "Manage context, pick the right model, measure with /usage." },
], 1.7, 3.8);

s = contentSlide(pres, "Training wrap-up: from first prompt to delivered PR",
  "Training-wide wrap-up. Walk through the four half-days: getting started, exploration and development, testing/debugging/integrations, and industrialization/security/delivery. Congratulate the group, then move to the quiz and survey.");
flow(s, [
  { head: "Half-day 1", body: "Get started with Claude Code" },
  { head: "Half-day 2", body: "Explore and develop" },
  { head: "Half-day 3", body: "Test, debug, integrate" },
  { head: "Half-day 4", body: "Industrialize, secure, deliver" },
], 1.9, 2.6);
footerNote(s, "You now have a workflow, not just a tool: plan, build, verify, review, deliver.");

s = contentSlide(pres, "Closing: quiz, survey and take-aways",
  "10-question quiz (docs/annexes/evaluation.md); feedback survey; hand over the cheat sheet (docs/annexes/aide-memoire.md) and repository access (solutions branch open to everyone). 10 minutes, individual.");
tag(s, "CLOSING  |  10 min  |  individual", K.accent4);
cards(pres, s, [
  { head: "10-question quiz", body: "Individual, from the evaluation annex." },
  { head: "Feedback survey", body: "Tell us what to keep and what to change." },
  { head: "Cheat sheet and repo", body: "Take the cheat sheet; the solutions branch is open to everyone." },
], 2.0, 3.6);

darkSlide(pres, "Thank you", "Questions, feedback and your next mission: put Claude Code to work.",
  "Closing slide. Stay available for questions after the survey.");

pres.writeFile({ fileName: "4-delivery-security-costs-case-study.pptx" }).then(() => console.log("wrote 4-delivery-security-costs-case-study.pptx"));
