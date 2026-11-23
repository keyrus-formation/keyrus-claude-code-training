// Half-day 1 deck: Getting started with Claude Code. Run: node half-day-1.js
const { THEME, newDeck, contentSlide, darkSlide, cards, stats } = require("./theme");
const { pres } = newDeck("Half-day 1 - Getting started with Claude Code");
const K = THEME.colors, SH = pres.ShapeType;
const txt = (s, t, o) => s.addText(t, { margin: 0, isTextBox: true, fontFace: "Calibri", color: K.dk1, fontSize: 16, valign: "top", align: "left", ...o });

// Horizontal process flow: [{head, body}]
function flow(s, steps, y = 2.0, h = 3.4) {
  const gap = 0.45, w = (12.1 - gap * (steps.length - 1)) / steps.length;
  steps.forEach((st, i) => {
    const x = 0.6 + i * (w + gap);
    s.addShape(SH.roundRect, { x, y, w, h, fill: { color: K.lt2 }, line: { color: K.lt2 }, rectRadius: 0.1 });
    txt(s, st.head, { x: x + 0.2, y: y + 0.2, w: w - 0.4, h: 0.7, fontSize: 20, bold: true, color: K.dk2 });
    txt(s, st.body, { x: x + 0.2, y: y + 1.0, w: w - 0.4, h: h - 1.2 });
    if (i < steps.length - 1) s.addShape(SH.rightArrow, { x: x + w + 0.05, y: y + h / 2 - 0.2, w: 0.35, h: 0.4, fill: { color: K.accent2 }, line: { color: K.accent2 } });
  });
}
// Table with header row
function table(s, rows, colW, y = 1.6, fs = 15) {
  const data = rows.map((r, i) => r.map(c => ({ text: c, options: i === 0 ? { bold: true, color: "FFFFFF", fill: { color: K.dk2 } } : { fill: { color: i % 2 ? "FFFFFF" : K.lt2 } } })));
  s.addTable(data, { x: 0.6, y, w: 12.1, colW, fontSize: fs, fontFace: "Calibri", color: K.dk1, align: "left", valign: "middle", border: { type: "solid", pt: 0.5, color: "D1D5DB" }, margin: 0.08 });
}
// Exercise / demo slide: badge on the left, numbered steps on the right
function task(kind, title, tag, dur, steps, notes, color = K.accent2) {
  const s = contentSlide(pres, title, notes);
  s.addShape(SH.roundRect, { x: 0.6, y: 1.7, w: 3.4, h: 4.6, fill: { color }, line: { color }, rectRadius: 0.1 });
  txt(s, kind, { x: 0.85, y: 1.95, w: 2.9, h: 0.5, fontSize: 18, bold: true, color: "FFFFFF" });
  txt(s, tag, { x: 0.85, y: 2.6, w: 2.9, h: 1.3, fontSize: 44, bold: true, color: "FFFFFF" });
  txt(s, dur, { x: 0.85, y: 4.2, w: 2.9, h: 1.0, fontSize: 28, color: "FFFFFF" });
  const h = Math.min(1.0, 4.6 / steps.length - 0.1);
  steps.forEach((t, i) => {
    const y = 1.7 + i * (4.6 / steps.length);
    s.addText(String(i + 1), { x: 4.4, y: y + 0.05, w: 0.5, h: 0.5, shape: SH.ellipse, fill: { color: K.dk2 }, color: "FFFFFF", bold: true, fontSize: 16, align: "center", valign: "middle", margin: 0, isTextBox: true });
    txt(s, t, { x: 5.1, y, w: 7.6, h: Math.max(h, 0.6), fontSize: 16, valign: "middle" });
  });
  return s;
}
function sectionSlide(title, sub, notes) { return darkSlide(pres, title, sub, notes); }

// 1 Title
darkSlide(pres, "Half-day 1: Getting started with Claude Code", "Introduction and fundamentals, prompting and context engineering. Keyrus Claude Code training for data consultants", "Session start time is up to the organiser. Duration: 4 hours including a 15 minute break.");

// 2 Agenda
{
  const s = contentSlide(pres, "Agenda: 4 hours, 2 themes", "Offsets are measured from the session start. The start time itself (e.g. 09:00 or 13:30) is decided by the organiser.");
  table(s, [
    ["Elapsed", "Min", "Sequence", "Format"],
    ["0:00", "15", "Welcome and expectations", "Discussion"],
    ["0:15", "35", "1.1 From chat assistant to agent", "Talk + demo"],
    ["0:50", "30", "1.2 Installation, configuration, permissions", "Demo + practice"],
    ["1:20", "30", "Exercise 1.1: first contact with RetailCo", "Practice"],
    ["1:50", "15", "Break", ""],
    ["2:05", "30", "2.1 Writing effective instructions + Exercise 1.2", "Talk + practice"],
    ["2:35", "25", "2.2 Context: window, CLAUDE.md, memory", "Talk + demo"],
    ["3:00", "30", "Exercise 1.3: write the project CLAUDE.md", "Practice"],
    ["3:30", "20", "2.3 Plan Mode + Exercise 1.4", "Demo + practice"],
    ["3:50", "10", "Wrap-up and preparing half-day 2", "Discussion"],
  ], [1.4, 0.9, 6.6, 3.2], 1.4, 15);
}

// 3 Welcome
{
  const s = contentSlide(pres, "Welcome: who is in the room?", "Round table, one sentence each: role, usual stack (SQL/dbt/Python/Spark), current AI usage (none / ChatGPT / Copilot / Cursor / Claude Code). Note the already-users on the board: they act as reference buddies. Set the ground rules: 50% practice, one running project, we break things on purpose, never real client data during the training.");
  cards(pres, s, [
    { head: "Your role", body: "Consultant, data engineer, analyst, architect" },
    { head: "Your stack", body: "SQL, dbt, Python, Spark, cloud warehouse" },
    { head: "Your AI usage", body: "None, ChatGPT, Copilot, Cursor or Claude Code" },
  ], 1.7, 3.2);
  txt(s, "Ground rules: 50% practice, one running project, we break things on purpose, no real client data.", { x: 0.6, y: 5.3, w: 12.1, h: 1.0, fontSize: 20, bold: true, color: K.dk2 });
}

// 4 Section 1
sectionSlide("Theme 1: Introduction and fundamentals", "From chat assistant to agent, installation, permissions");

// 5 LLM vs agent
{
  const s = contentSlide(pres, "A chat answers. An agent works.", "An LLM (Large Language Model) in chat mode receives text and returns text. You copy the code, run it, paste the error back. An agent receives a goal, then loops until the goal is reached or it needs you.");
  s.addShape(SH.roundRect, { x: 0.6, y: 1.7, w: 5.8, h: 4.4, fill: { color: K.lt2 }, line: { color: K.lt2 }, rectRadius: 0.1 });
  txt(s, "Chat assistant", { x: 0.9, y: 1.95, w: 5.2, h: 0.5, fontSize: 24, bold: true, color: K.dk2 });
  txt(s, "Receives text, returns text.\n\nYou copy the code, run it and paste the error back.", { x: 0.9, y: 2.7, w: 5.2, h: 3.0, fontSize: 20 });
  s.addShape(SH.roundRect, { x: 6.9, y: 1.7, w: 5.8, h: 4.4, fill: { color: K.accent2 }, line: { color: K.accent2 }, rectRadius: 0.1 });
  txt(s, "Agent (Claude Code)", { x: 7.2, y: 1.95, w: 5.2, h: 0.5, fontSize: 24, bold: true, color: "FFFFFF" });
  txt(s, "Receives a goal, then loops: gathers context, acts with tools, checks the result.\n\nStops when done, or when it needs you.", { x: 7.2, y: 2.7, w: 5.2, h: 3.0, fontSize: 20, color: "FFFFFF" });
}

// 6 Agent loop
{
  const s = contentSlide(pres, "The agent loop: gather, act, verify", "You can interrupt with Esc and redirect at any time. The loop continues until 'done' or a question to the human.");
  flow(s, [
    { head: "1. Gather context", body: "Read files, search the repository" },
    { head: "2. Act", body: "Edit files, run a command" },
    { head: "3. Verify", body: "Tests, output, errors" },
  ], 1.9, 2.8);
  txt(s, "Loops until done, or until a question for the human. Press Esc at any time to interrupt and redirect.", { x: 0.6, y: 5.2, w: 12.1, h: 1.0, fontSize: 20, bold: true, color: K.dk2 });
}

// 7 Comparison table
{
  const s = contentSlide(pres, "What changes when the model can act", "Main risk shifts from a wrong answer to a wrong action (overwritten file, dangerous command). Your role becomes project manager and reviewer.");
  table(s, [
    ["", "Chat assistant", "Agent (Claude Code)"],
    ["Access to code", "What you paste", "The whole repository, on demand"],
    ["Execution", "None", "Shell commands, tests, dbt, git"],
    ["Verification", "By you", "By itself, if you give it the means"],
    ["Unit of work", "One answer", "One task (dozens of actions)"],
    ["Main risk", "Wrong answer", "Wrong action"],
    ["Your role", "Question writer", "Project manager + reviewer"],
  ], [2.6, 4.2, 5.3], 1.6, 18);
}

// 8 Tools and surfaces
{
  const s = contentSlide(pres, "Tools and where to run Claude Code", "Show the tools in the demo without going into detail. MCP and skills are covered in half-day 3. Same engine and same configuration files everywhere.");
  cards(pres, s, [
    { head: "Built-in tools", body: "Read, Grep, Glob, Edit, Write, Bash, WebFetch, WebSearch, subagents" },
    { head: "Extensions", body: "MCP servers and skills, covered in half-day 3" },
    { head: "Where it runs", body: "Terminal (our focus), VS Code, JetBrains, desktop, web, Slack, CI" },
  ], 1.7, 3.6);
  txt(s, "Same engine, same configuration files everywhere.", { x: 0.6, y: 5.6, w: 12.1, h: 0.7, fontSize: 20, bold: true, color: K.dk2 });
}

// 9 Demo 1
task("DEMO", "Demo: Claude explores RetailCo", "10 min", "Default mode, prompt on screen", [
  "Prompt: \"what does this project do? give me the architecture in 5 lines and the command to run everything\"",
  "Point out: Claude received nothing but the question, and chose to read the README, pyproject.toml, and list src/",
  "Prompt: \"run the unit tests and tell me whether they pass\"",
  "Claude asks permission to run pytest: introduces the permissions section",
], "DEMO SCRIPT (10 min). In the RetailCo repository, default mode, project the prompt:\n  que fait ce projet ? donne-moi l'architecture en 5 lignes et la commande pour tout lancer\n(French for: what does this project do? give me the architecture in 5 lines and the command to run everything.)\nComment live: Claude received nothing but the question; it decides on its own to read the README and pyproject.toml and to list src/. Point out the tool calls displayed.\nThen:\n  lance les tests unitaires et dis-moi s'ils passent\n(French for: run the unit tests and tell me whether they pass.)\nClaude asks permission to run pytest (or not, if the project's allow rule covers it): a good opportunity to introduce permissions.", K.accent3);

// 10 Trainer Q&A
{
  const s = contentSlide(pres, "Which model runs behind the scenes?", "Frequent question. /model lets you choose. We come back to costs in half-day 4. Do not promise that the agent understands the business: it infers from what it reads, hence the importance of CLAUDE.md (after the break).");
  cards(pres, s, [
    { head: "Opus", body: "Complex reasoning" },
    { head: "Sonnet", body: "Default: most coding tasks" },
    { head: "Haiku", body: "Simple and fast tasks" },
  ], 1.7, 2.8);
  txt(s, "Switch with /model. The agent infers the business from what it reads: it does not truly understand it. That is why CLAUDE.md matters.", { x: 0.6, y: 4.9, w: 12.1, h: 1.3, fontSize: 20, bold: true, color: K.dk2 });
}

// 11 Installation
{
  const s = contentSlide(pres, "Installation in three steps", "Normally done beforehand. Native install recommended with automatic updates. On native Windows, Git for Windows is recommended (otherwise Claude Code uses PowerShell as its shell); WSL does not need it. Sign-in options: Claude account (Pro, Max, Team, Enterprise), Claude Console (API), or cloud provider (Amazon Bedrock, Google Cloud, Microsoft Foundry). Alternatives: brew install --cask claude-code, winget install Anthropic.ClaudeCode.");
  flow(s, [
    { head: "Install", body: "macOS, Linux, WSL: curl -fsSL https://claude.ai/install.sh | bash\nWindows: irm https://claude.ai/install.ps1 | iex" },
    { head: "Check", body: "claude --version" },
    { head: "Sign in", body: "First launch of claude: Claude account, Console API or cloud provider" },
  ], 1.8, 3.6);
}

// 12 Essential commands
{
  const s = contentSlide(pres, "Essential commands", "These are on the cheat sheet. claude -p is the basis for automation (half-days 3 and 4).");
  table(s, [
    ["Command", "Effect"],
    ["claude / claude \"task\"", "Interactive session, optionally with a first prompt"],
    ["claude -p \"question\"", "Headless mode: answers then exits (automation)"],
    ["claude -c / claude -r", "Resume last conversation / pick a conversation"],
    ["/clear   /context   /usage", "Empty context / see the window / see consumption"],
    ["/model   /effort", "Choose the model and the thinking level"],
    ["Esc   Esc x2 or /rewind", "Interrupt Claude / go back to a checkpoint"],
    ["Shift+Tab   @file   !cmd", "Cycle modes / reference a file / run a shell command"],
  ], [4.2, 7.9], 1.6, 16);
}

// 13 Permission modes
{
  const s = contentSlide(pres, "Six permission modes", "default is the training mode. bypassPermissions only in an isolated container or VM. Stress: deny rules apply in every mode, including bypassPermissions. Writes to .git, .claude, .mcp.json are never auto-approved (except in bypassPermissions).");
  table(s, [
    ["Mode", "Runs without asking", "Use"],
    ["default", "Reads only", "Discovery, sensitive code (training mode)"],
    ["acceptEdits", "Reads + file edits", "Iterating on code you review as you go"],
    ["plan", "Reads, no modifications", "Analyse and plan before touching code"],
    ["auto", "Everything, safety classifier", "Long tasks, if available and allowed"],
    ["dontAsk", "Reads + pre-approved tools", "CI and locked-down scripts"],
    ["bypassPermissions", "Everything", "Only in an isolated container or VM"],
  ], [2.8, 4.0, 5.3], 1.6, 16);
}

// 14 Settings demo
{
  const s = contentSlide(pres, "Demo: allow, ask, deny in settings.json", "DEMO. Open .claude/settings.json and read it with the room. allow: pytest, ruff, local dbt, read-only git. ask: git commit, git push, dbt on the Snowflake target. deny: reading .env and credential profiles, modifying data/raw/, curl/wget. Priority of settings: managed (enforced by IT) > command line > .claude/settings.local.json (personal, not committed) > .claude/settings.json (team, committed) > ~/.claude/settings.json (user). Live demonstration: 'lis le fichier .env' (read the .env file) is refused. First building block of the security part (half-day 4).");
  cards(pres, s, [
    { head: "allow", body: "pytest, ruff, local dbt, read-only git: no friction on safe actions" },
    { head: "ask", body: "git commit, git push, dbt on Snowflake: human confirmation" },
    { head: "deny", body: "Reading .env and credentials, editing data/raw/, curl and wget" },
  ], 1.7, 3.4);
  txt(s, "Live: ask Claude to read the .env file. Refused.", { x: 0.6, y: 5.5, w: 12.1, h: 0.7, fontSize: 20, bold: true, color: K.dk2 });
}

// 15 Priority
{
  const s = contentSlide(pres, "Which setting wins?", "Priority order of settings, from strongest to weakest.");
  flow(s, [
    { head: "Managed", body: "Enforced by IT" },
    { head: "Command line", body: "Flags for this run" },
    { head: "settings.local", body: "Personal, not committed" },
    { head: "settings.json", body: "Team, committed" },
    { head: "~/.claude", body: "User defaults" },
  ], 2.0, 2.6);
  txt(s, "Strongest on the left, weakest on the right.", { x: 0.6, y: 5.2, w: 12.1, h: 0.7, fontSize: 20, bold: true, color: K.dk2 });
}

// 16 Exercise 1.1
task("EXERCISE", "Exercise 1.1: first contact with RetailCo", "Ex 1.1", "30 min, individual", [
  "Launch claude at the repo root, check model and folder with /status",
  "Ask what the project does, what the data sources are, and run the tests and dbt build",
  "Ask Claude to read .env: what happens and why?",
  "Cycle the permission modes with Shift+Tab and note their names",
  "Type /context: what already fills the window?",
], "Goal: everyone has a working session, has seen Claude read, execute and answer, and has met a permission request. Walk the room: unblock failed installations first. After 20 min, have 2 or 3 people share their answers to 'what surprised you?'. Exercise sheet: exercises/HD1_getting_started.md. Stretch goal: claude -p with --output-format json, what could this mode be used for?");

// 17 Break
sectionSlide("Break", "15 minutes. Back at 2:05");

// 18 Section 2
sectionSlide("Theme 2: Prompting and context engineering", "Instructions, context window, CLAUDE.md, Plan Mode");

// 19 Prompt = ticket
{
  const s = contentSlide(pres, "A good prompt is a good ticket", "A good prompt for an agent is not an incantation, it is a good Jira ticket: context, goal, constraints, definition of done. Formula to remember: Context, Goal, Constraints, Verification.");
  flow(s, [
    { head: "Context", body: "Where, which files, what exists" },
    { head: "Goal", body: "What outcome you want" },
    { head: "Constraints", body: "What must not change" },
    { head: "Verification", body: "How we know it is done" },
  ], 2.0, 2.6);
  txt(s, "Treat the prompt like a Jira ticket, not an incantation.", { x: 0.6, y: 5.2, w: 12.1, h: 0.7, fontSize: 20, bold: true, color: K.dk2 });
}

// 20 Bad vs good
{
  const s = contentSlide(pres, "Bad prompt, good prompt", "Walk through each row. Further principles: point to files with @, give a verification criterion, set constraints, give an example, one task at a time, let it explore first.");
  table(s, [
    ["Principle", "Bad", "Good"],
    ["Be specific", "fix the bug", "In transform.clean_orders, duplicates keep the old version: keep the latest updated_at"],
    ["Point to files", "look at the orders model", "look at @dbt_project/models/marts/fct_orders.sql"],
    ["Verify", "add tests", "add a failing test, fix, then run pytest -q until green"],
    ["Example", "format the amounts", "'1 234,50' becomes 1234.5, '' becomes None"],
  ], [2.4, 3.2, 6.5], 1.6, 16);
}

// 21 More levers
{
  const s = contentSlide(pres, "Four more levers", "Constraints example: without adding a dependency, SQL compatible with Snowflake and DuckDB, do not change the public API. Let it explore first: read the relevant code and explain how X should fit in, do not modify anything.");
  cards(pres, s, [
    { head: "Constraints", body: "No new dependency. SQL for Snowflake and DuckDB. Keep the public API" },
    { head: "One task at a time", body: "Three requests with verification between each" },
    { head: "Explore first", body: "Read, explain, do not modify anything" },
    { head: "Correct early", body: "Esc as soon as the direction is wrong" },
  ], 1.7, 3.6);
  txt(s, "Also: paste the full error or a screenshot, and ask Claude to interview you when the need is vague.", { x: 0.6, y: 5.6, w: 12.1, h: 0.8, fontSize: 18, bold: true, color: K.dk2 });
}

// 22 Exercise 1.2
task("EXERCISE", "Exercise 1.2: rewrite weak prompts", "Ex 1.2", "15 min, built in", [
  "Take the 3 weak prompts: add tests / pipeline is slow, optimise / make a dbt model for sales by product",
  "Rewrite each with Context, Goal, Constraints, Verification",
  "Test both versions, with /clear between each",
  "Compare number of actions and quality of result. Do not commit: git checkout . afterwards",
], "Participants rewrite 3 weak prompts from the exercise sheet, test them, and compare the number of actions and the quality of the result. Debrief: have the best prompt in the room read aloud.");

// 23 Context window
{
  const s = contentSlide(pres, "The context window is your budget", "Everything Claude knows during a session fits in its context window: system instructions, CLAUDE.md, history, contents of files read, command outputs. Fuller means each exchange costs more because everything is sent again with every request, and old off-topic information dilutes attention.");
  stats(pres, s, [
    { value: "100%", label: "of the history is sent again with every request" },
    { value: "Cost", label: "grows as the window fills up" },
    { value: "Focus", label: "drops when old, off-topic content piles up" },
  ], 1.9);
}

// 24 Context habits
{
  const s = contentSlide(pres, "Four habits to manage context", "/rename before /clear to find the session again. /compact example: /compact keep the modified files and the test results. Subagents are covered in half-day 3.");
  cards(pres, s, [
    { head: "/context", body: "See what fills the window" },
    { head: "/clear", body: "Between two unrelated tasks. It is free" },
    { head: "/compact", body: "Summarise a long session, keep the essentials" },
    { head: "Subagents", body: "Delegate verbose work: only the summary comes back" },
  ], 1.7, 3.4);
}

// 25 CLAUDE.md
{
  const s = contentSlide(pres, "CLAUDE.md: the project memory", "Every session starts blank. CLAUDE.md is a Markdown file loaded automatically at startup. All files found are concatenated, not replaced. A file can import another with @path/file. There is also an automatic memory that Claude writes from your corrections; /memory lets you view and edit everything.");
  table(s, [
    ["Location", "Scope", "Committed?"],
    ["Company policy (/etc/claude-code/CLAUDE.md)", "Whole organisation, enforced by IT", "n/a"],
    ["~/.claude/CLAUDE.md", "You, all your projects", "No"],
    ["./CLAUDE.md", "The project, the whole team", "Yes"],
    ["./CLAUDE.local.md", "You, this project (in .gitignore)", "No"],
    ["subfolder/CLAUDE.md", "Loaded when working in that subfolder", "Yes"],
    [".claude/rules/*.md with paths:", "Only for matching files", "Yes"],
  ], [5.4, 4.8, 1.9], 1.6, 16);
}

// 26 What goes in
{
  const s = contentSlide(pres, "What goes in CLAUDE.md, and what does not", "CLAUDE.md is context, not a constraint. Guaranteed rules belong in deny permissions or hooks. Aim for fewer than 200 lines: beyond that, adherence drops and cost rises.");
  s.addShape(SH.roundRect, { x: 0.6, y: 1.7, w: 5.9, h: 4.0, fill: { color: K.lt2 }, line: { color: K.lt2 }, rectRadius: 0.1 });
  txt(s, "Put in", { x: 0.9, y: 1.9, w: 5.3, h: 0.5, fontSize: 22, bold: true, color: K.accent2 });
  txt(s, "Exact build and test commands\nBusiness pitfalls (French amount format, 2 payments per order)\nTeam conventions (dbt naming, commit format)\nProhibitions (never run dbt on prod)", { x: 0.9, y: 2.5, w: 5.3, h: 3.1, fontSize: 16 });
  s.addShape(SH.roundRect, { x: 6.8, y: 1.7, w: 5.9, h: 4.0, fill: { color: K.lt2 }, line: { color: K.lt2 }, rectRadius: 0.1 });
  txt(s, "Leave out", { x: 7.1, y: 1.9, w: 5.3, h: 0.5, fontSize: 22, bold: true, color: K.accent6 });
  txt(s, "A description of every file: Claude can read\nLong, rare procedures: use skills (half-day 3)\nRules that must be guaranteed: use deny permissions or hooks", { x: 7.1, y: 2.5, w: 5.3, h: 3.1, fontSize: 16 });
  txt(s, "Target: fewer than 200 lines.", { x: 0.6, y: 5.95, w: 12.1, h: 0.6, fontSize: 20, bold: true, color: K.dk2 });
}

// 27 Rules demo
{
  const s = contentSlide(pres, "Demo: path-scoped rules", "DEMO (5 min). Show .claude/rules/dbt.md: thanks to paths:, these rules enter the context only when Claude touches a dbt file.");
  stats(pres, s, [
    { value: "5 min", label: "Demo: open .claude/rules/dbt.md" },
    { value: "paths:", label: "Front-matter that scopes the rules to matching files" },
    { value: "0 tokens", label: "Spent on dbt rules until Claude touches a dbt file" },
  ], 2.0);
}

// 28 Exercise 1.3
task("EXERCISE", "Exercise 1.3: write the project CLAUDE.md", "Ex 1.3", "30 min, practice", [
  "Run /init and read the generated CLAUDE.md",
  "Question Claude about the data (not the code) to find the business pitfalls",
  "Add Business pitfalls and Security sections, under 80 lines",
  "Test: /clear then ask how to join payments to orders. Is your CLAUDE.md used?",
  "Create CLAUDE.local.md and check Git ignores it",
], "Participants critique and enrich the /init output with the business pitfalls they discover. Reference solution: solutions/CLAUDE.md. Do NOT show it before the end: the point is to see that /init does not find the business pitfalls on its own. The pitfalls listed in the solution are exactly the bugs hunted in half-day 3: this is intentional, and we will come back to it.");

// 29 Plan mode
{
  const s = contentSlide(pres, "Plan Mode: think before you write", "Plan Mode (Shift+Tab until 'plan', or claude --permission-mode plan): Claude explores and proposes a plan without modifying anything. You approve, amend or reject before any write. Add 'think deeply' for complex topics. Decompose: one task = one verifiable result. A 15-step plan is split into 3 sessions with /clear between them, the plan being saved in a file (PLAN.md).");
  flow(s, [
    { head: "Explore", body: "Read X and Y, explain, change nothing" },
    { head: "Plan", body: "Plan Mode: steps, files, tests" },
    { head: "Implement", body: "Step by step" },
    { head: "Verify", body: "Tests, dbt build, diff" },
    { head: "Commit", body: "Once reviewed" },
  ], 1.9, 2.8);
  txt(s, "One task = one verifiable result. Split big plans into sessions and save the plan in PLAN.md.", { x: 0.6, y: 5.2, w: 12.1, h: 1.0, fontSize: 20, bold: true, color: K.dk2 });
}

// 30 Exercise 1.4
task("EXERCISE", "Exercise 1.4: add --since in Plan Mode", "Ex 1.4", "15 min, in pairs", [
  "Switch to Plan Mode with Shift+Tab",
  "Ask for a plan for a --since YYYY-MM-DD option: files, tests, edge cases",
  "Have your buddy approve the plan, and amend it at least once",
  "Leave Plan Mode, implement, run pytest -q",
  "Review git diff: was everything foreseen in the plan?",
], "Add to the pipeline a --since YYYY-MM-DD option that loads only orders after a given date. Plan Mode is mandatory and the plan must be approved by the buddy before implementation.");

// 31 Recap
{
  const s = contentSlide(pres, "Recap: three ideas to keep", "Have the room state the 3 ideas they retain first, then complete with these.");
  cards(pres, s, [
    { head: "The agent acts", body: "So rely on permissions and review every diff" },
    { head: "Context is quality and cost", body: "Keep CLAUDE.md short and use /clear often" },
    { head: "Plan before coding", body: "Use Plan Mode for any non-trivial task" },
  ], 1.7, 3.8);
}

// 32 Closing
darkSlide(pres, "See you in half-day 2", "Keep your CLAUDE.md. Optional homework: read sql/legacy/customer_ltv.sql without Claude and note what looks suspicious.", "Wrap-up (10 min). For half-day 2: keep your CLAUDE.md; those who wish read the legacy query sql/legacy/customer_ltv.sql (without Claude!) and note what looks suspicious.");

pres.writeFile({ fileName: "half-day-1.pptx" }).then(f => console.log("wrote", f));
