// Half-day 3 deck: Make it reliable and equip it. Run from slides/: node half-day-3.js
const { THEME, newDeck, contentSlide, darkSlide, cards, stats } = require("./theme");
const { pres } = newDeck("Half-day 3 - Make it reliable and equip it");
const K = THEME.colors, SH = pres.ShapeType;

// ---- local helpers (kept here so theme.js stays untouched) ----
function flow(s, steps, y = 2.0, h = 3.6) {
  const gap = 0.45, w = (12.1 - gap * (steps.length - 1)) / steps.length;
  steps.forEach((st, i) => {
    const x = 0.6 + i * (w + gap);
    s.addShape(SH.roundRect, { x, y, w, h, fill: { color: K.lt2 }, line: { color: K.lt2 }, rectRadius: 0.1 });
    s.addText(st.head, { x: x + 0.2, y: y + 0.2, w: w - 0.4, h: 0.7, fontSize: 20, bold: true, color: K.dk2, margin: 0, valign: "top", isTextBox: true });
    s.addText(st.body, { x: x + 0.2, y: y + 1.0, w: w - 0.4, h: h - 1.2, fontSize: 16, color: K.dk1, margin: 0, valign: "top", isTextBox: true });
    if (i < steps.length - 1) s.addShape(SH.rightArrow, { x: x + w + 0.05, y: y + h / 2 - 0.15, w: gap - 0.1, h: 0.3, fill: { color: K.accent2 }, line: { color: K.accent2 } });
  });
}
function table(s, rows, colW, y = 1.6, fs = 14) {
  const data = rows.map((r, i) => r.map((c) => ({ text: String(c), options: i === 0
    ? { bold: true, color: "FFFFFF", fill: { color: K.dk2 }, fontSize: fs, align: "left", valign: "middle" }
    : { color: K.dk1, fill: { color: i % 2 ? "FFFFFF" : K.lt2 }, fontSize: fs, align: "left", valign: "middle" } })));
  s.addTable(data, { x: 0.6, y, w: 12.1, colW, border: { type: "solid", pt: 0.5, color: "D1D5DB" }, margin: [0.06, 0.1, 0.06, 0.1], fontFace: "Calibri" });
}
function callout(s, text, y = 5.9, h = 0.8, color = K.accent2) {
  s.addShape(SH.roundRect, { x: 0.6, y, w: 12.1, h, fill: { color }, line: { color }, rectRadius: 0.1 });
  s.addText(text, { x: 0.85, y, w: 11.6, h, fontSize: 18, bold: true, color: "FFFFFF", margin: 0, valign: "middle", isTextBox: true });
}
function code(s, text, y = 1.7, h = 2.6) {
  s.addShape(SH.roundRect, { x: 0.6, y, w: 12.1, h, fill: { color: K.dk1 }, line: { color: K.dk1 }, rectRadius: 0.08 });
  s.addText(text, { x: 0.85, y: y + 0.1, w: 11.6, h: h - 0.2, fontSize: 14, fontFace: "Consolas", color: "E5E7EB", margin: 0, valign: "top", isTextBox: true });
}
function tag(s, text, color = K.accent3) { // exercise / demo marker, top right
  s.addText(text, { x: 9.6, y: 0.5, w: 3.1, h: 0.5, shape: SH.roundRect, rectRadius: 0.1, fill: { color }, color: "FFFFFF", bold: true, fontSize: 16, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
const N = (title, notes) => contentSlide(pres, title, notes);

// 1 Title
darkSlide(pres, "Half-day 3: Make it reliable and equip it", "Testing, debugging and quality, then integrations and automation with Claude Code",
  "Session start time is up to the organiser (e.g. 09:00 or 13:30). 4-hour session, timings are offsets from the start.");

// 2 Agenda
let s = N("Agenda: 4 hours, two themes", "Theme 5: Testing, debugging & quality. Theme 6: Integrations and automation. The break is a break: let people stretch and refill coffee.");
table(s, [
  ["Start", "Min", "Sequence", "Format"],
  ["0:00", "20", "5.1 Testing with an agent: test first", "Talk"],
  ["0:20", "55", "Exercise 3.1: the 4-bug hunt", "Hands-on"],
  ["1:15", "15", "5.2 Data quality and validating generated code", "Talk"],
  ["1:30", "25", "Exercise 3.2: Python + dbt quality checks", "Hands-on"],
  ["1:55", "15", "Break", ""],
  ["2:10", "25", "6.1 Extending Claude Code: the toolbox", "Talk"],
  ["2:35", "25", "6.2 MCP and Data tools + Exercise 3.3", "Demo + hands-on"],
  ["3:00", "40", "6.3 Skills, hooks, automation + Exercise 3.4", "Demo + hands-on"],
  ["3:40", "20", "Wrap-up and preparation for HD4", "Discussion"],
], [1.2, 0.9, 7.2, 2.8], 1.5, 15);

// 3 Section 5
darkSlide(pres, "Theme 5: Testing, debugging and quality", "0:00 to 1:55", "Section opener. 5.1 (20 min talk), Exercise 3.1 (55 min), 5.2 (15 min talk), Exercise 3.2 (25 min).");

// 4 Green suite
s = N("A green test suite only proves what it tests",
  "Recall the question left at the end of HD2: the 4 Python tests pass, and yet the pipeline loses money. An agent that writes code AND its tests can write tests that validate its own mistakes.");
stats(pres, s, [{ value: "4 / 4", label: "unit tests pass on the training pipeline" }, { value: "4", label: "bugs hidden in the pipeline and the dbt model" }, { value: "?", label: "who checks that the tests themselves are right" }], 1.8);
callout(s, "An agent that writes code and its tests can validate its own mistakes", 5.4);

// 5 Five rules
s = N("Five ground rules with Claude Code",
  "1 TDD: a test that has never failed has proven nothing. 2 Edge cases come from you: French formats, empty values, duplicates, currencies, time zones, split payments. 3 Put in CLAUDE.md: 'never modify an existing test to make it pass; flag it instead'. 4 Forbid try/except: pass, silent errors=\"coerce\", DISTINCT that hides a wrong join. 5 Human review is the last line of defence; for fresh eyes use the data-reviewer subagent.");
cards(pres, s, [
  { head: "Test first", body: "Show the test failing, then fix" },
  { head: "Your edge cases", body: "Formats, blanks, duplicates, FX" },
  { head: "Tests stay put", body: "Never edit a test to pass it" },
  { head: "No workarounds", body: "No bare except, no masking DISTINCT" },
  { head: "Review the diff", body: "Human, or the data-reviewer subagent" },
], 1.7, 4.4);

// 6 TDD loop
s = N("Test first: a test that never failed proves nothing",
  "Prompt: 'write a test that reproduces the bug, show me it fails, then fix it'.");
flow(s, [
  { head: "Write the test", body: "Reproduces the bug on the current code" },
  { head: "See it fail", body: "Red proves the test can catch the bug" },
  { head: "Fix the cause", body: "Smallest change, no unrelated edits" },
  { head: "See it pass", body: "Whole suite green, impact quantified" },
], 1.8, 3.4);
callout(s, "Prompt: \"write a test that reproduces the bug, show me it fails, then fix it\"", 5.7);

// 7 Debugging 4 steps
s = N("Debugging in 4 steps",
  "Reproduce: 'here is the symptom: ... write the smallest script or test that reproduces it'. Locate: 'find the root cause, not the symptom; explain it before proposing a fix'. Fix: 'fix only the cause, without unrelated changes'. Prove: 'the reproduction test passes, the whole suite passes, and here is the quantified impact on the data'.");
flow(s, [
  { head: "1 Reproduce", body: "Smallest script or test that shows the symptom" },
  { head: "2 Locate", body: "Root cause, not symptom. Explain before fixing" },
  { head: "3 Fix", body: "Only the cause, nothing unrelated" },
  { head: "4 Prove", body: "Repro test and suite pass, impact in numbers" },
], 1.8, 4.2);

// 8 Raw material
s = N("Give Claude the raw material, never a paraphrase",
  "Provide the full error message, the dbt build output, a sample of rows. Do not paraphrase.");
cards(pres, s, [
  { head: "Do paste", body: "Full error message and stack trace\nOutput of dbt build\nA sample of real rows" },
  { head: "Do not paste", body: "Your summary of the error\n\"It fails on the join\"\nA guess presented as a fact" },
], 1.7, 3.8);
callout(s, "Better input gives a better root cause", 5.8);

// 9 Exercise 3.1
s = N("The business says: revenue does not match accounting",
  "Exercise 3.1, 55 min, individual then group debrief (10 min). Participants have Claude Code, the red dbt build and their CLAUDE.md. For each bug: a failing test, the fix, the quantified impact. Rules: no editing a test to pass it, no DISTINCT to hide a duplicate, no swallowed exception. TRAINER SHEET (do not hand out): B1 transform.parse_amount: '1 234,50' keeps the thousands space, ValueError swallowed, None: 366 orders without amount, about 572k EUR ignored. B2 transform.clean_orders: ascending sort + keep='first' keeps the OLDEST version: 1,000 orders with stale status, return rate underestimated. B3 clean_orders: divides by the rate instead of multiplying (FX_TO_EUR = value of one unit in EUR): 4,058 USD/CHF orders wrong, 100 USD gives 108.70 instead of 92. B4 fct_orders.sql and build_order_facts: direct join on payments (2 payments for some orders), fan-out: 2,796 duplicate rows, revenue inflated by about 901k EUR, dbt test unique_fct_orders_order_id fails. HINTS every 15 min: 1 compare count(*) and count(distinct order_id) in fct_orders. 2 how many non-empty amounts become None after parse_amount? 3 take an order present twice in orders.csv: which status does the pipeline keep? 4 100 USD is how many euros?");
tag(s, "Exercise 3.1 | 55 min");
cards(pres, s, [
  { head: "Revenue too high", body: "fct_orders is above accounting" },
  { head: "Large B2B orders", body: "Some show no amount at all" },
  { head: "Odd dollar amounts", body: "USD conversions look wrong" },
  { head: "Return rate too low", body: "Customer service sees more" },
], 1.7, 3.0);
callout(s, "For each bug: a failing test, the fix, the quantified impact. Do not edit tests, do not add DISTINCT, do not swallow exceptions.", 5.2, 1.2, K.accent4);

// 10 Debrief table
s = N("Debrief: four bugs, real money",
  "Debrief 10 min. How many bugs found? Which did Claude find spontaneously, which thanks to a business question? Usually B4 is found quickly thanks to the red dbt test; B1 and B3 thanks to the CLAUDE.md enriched in HD1; B2 is the one most often missed. Solutions: solutions/src/retail_pipeline/transform.py, solutions/tests/test_regressions.py (9 tests, 6 fail on the original code), solutions/dbt_project/models/marts/fct_orders.sql.");
table(s, [
  ["#", "Where", "Bug", "Impact"],
  ["B1", "parse_amount", "Thousands space kept, error swallowed, None", "366 orders, about 572k EUR ignored"],
  ["B2", "clean_orders", "Sort ascending + keep first keeps the oldest", "1,000 stale statuses, returns missed"],
  ["B3", "clean_orders", "Divides by FX rate instead of multiplying", "4,058 USD/CHF orders, 100 USD = 108.70"],
  ["B4", "fct_orders", "Join on payments fans out rows", "2,796 duplicates, about 901k EUR inflated"],
], [0.8, 2.3, 4.7, 4.3], 1.7, 16);

// 11 Chart
s = N("Debrief: the bugs touch thousands of rows",
  "Rows affected on the training dataset. Message: business context is what lets the agent find business bugs. The pitfalls in the model-answer CLAUDE.md match the bugs exactly.");
s.addChart(pres.charts.BAR, [{ name: "Rows affected", labels: ["B1 amounts lost", "B2 stale status", "B3 wrong FX", "B4 duplicates"], values: [366, 1000, 4058, 2796] }],
  { x: 0.6, y: 1.5, w: 7.4, h: 5.2, barDir: "bar", chartColors: [K.accent2], showValue: true, dataLabelFontSize: 14, catAxisLabelFontSize: 14, valAxisLabelFontSize: 12, valGridLine: { style: "none" }, showLegend: false });
s.addShape(SH.roundRect, { x: 8.4, y: 1.7, w: 4.3, h: 4.6, fill: { color: K.lt2 }, line: { color: K.lt2 }, rectRadius: 0.1 });
s.addText("Business context finds business bugs", { x: 8.65, y: 1.95, w: 3.8, h: 1.2, fontSize: 22, bold: true, color: K.dk2, margin: 0, valign: "top", isTextBox: true });
s.addText("The pitfalls written in CLAUDE.md match these bugs exactly", { x: 8.65, y: 3.3, w: 3.8, h: 2.6, fontSize: 16, color: K.dk1, margin: 0, valign: "top", isTextBox: true });

// 12 Section 5.2 two kinds of tests
s = N("Two kinds of tests, two moments",
  "5.2, 15 min talk. Unit tests check that the code does what is expected on constructed cases; data tests check that the data respects the rules on every run.");
table(s, [
  ["", "Unit tests (pytest)", "Data tests (dbt, Python checks)"],
  ["Verify", "The code on constructed cases", "The data, on every run"],
  ["Examples", "parse_amount('1 234,50') == 1234.5", "unique, not_null, accepted_values, relationships, payments vs orders"],
  ["When", "On every change (CI)", "On every load (pipeline, dbt build)"],
], [1.8, 4.6, 5.7], 1.7, 16);
callout(s, "Code is tested on every change, data on every load", 5.4);

// 13 Source anomalies
s = N("Flag source anomalies, never fix them silently",
  "Checks that detect anomalies in the source: to be flagged, not silently corrected. 209 negative amounts, 87 orders dated 2031, 212 empty amounts, 2% duplicate customers, upper-case emails.");
stats(pres, s, [{ value: "209", label: "negative amounts" }, { value: "87", label: "orders dated 2031" }, { value: "212", label: "empty amounts" }, { value: "2%", label: "duplicate customers" }], 1.9);
callout(s, "Also seen: upper-case emails. Report them, let the business decide", 5.2);

// 14 Checklist
s = N("Validating generated code: a 5-point checklist",
  "1 Existing tests pass AND a new test covers the change. 2 The diff touches only what was requested. 3 Key figures reconciled with an independent source (row counts, checksums). 4 No silent behaviour added (swallowed exception, masking default). 5 Human review, ideally supported by an independent review (data-reviewer subagent, see HD4).");
cards(pres, s, [
  { head: "Tests", body: "Old pass, new one covers the change" },
  { head: "Scope", body: "Diff touches only what was asked" },
  { head: "Reconcile", body: "Row counts and checksums vs a source" },
  { head: "No silence", body: "No swallowed error or masking default" },
  { head: "Review", body: "Human plus independent subagent" },
], 1.7, 4.4);

// 15 Exercise 3.2
s = N("Complete the quality checks in Python and dbt",
  "Exercise 3.2, 25 min. Complete quality.py (4 TODO functions) and add missing dbt tests, including a singular test reconciling payments with orders. Solutions: solutions/src/retail_pipeline/quality.py and solutions/dbt_project/tests/assert_payments_reconcile_with_orders.sql. In step 1, run /data-quality-audit and compare with what is known.");
tag(s, "Exercise 3.2 | 25 min");
cards(pres, s, [
  { head: "Audit", body: "Run /data-quality-audit on orders.csv and compare with what you know" },
  { head: "Python", body: "Complete the 4 TODO functions in quality.py, with unit tests" },
  { head: "dbt", body: "Add relationships and a singular payments reconciliation test" },
], 1.7, 3.6);
callout(s, "Source anomalies are flagged, not deleted. Where and how do you flag them?", 5.6);

// 16 Break
darkSlide(pres, "Break", "15 minutes", "Break at 1:55, back at 2:10.");

// 17 Section 6
darkSlide(pres, "Theme 6: Integrations and automation", "2:10 to 4:00", "6.1 toolbox (25 min), 6.2 MCP (25 min), 6.3 skills, hooks, automation (40 min), wrap-up (20 min).");

// 18 Toolbox
s = N("The Claude Code toolbox: seven building blocks",
  "CLAUDE.md/rules: permanent instructions. Skill: reusable procedure (.claude/skills/<name>/SKILL.md), invoked with /name or loaded when its description matches. Subagent: specialised assistant with own context, tools, model (.claude/agents/<name>.md). Hook: shell command run deterministically at a point in the cycle. MCP: standard protocol to plug external tools. Plugin: package bundling skills, agents, hooks, MCP for sharing. Headless mode: claude -p. Old custom commands (.claude/commands/*.md) still work and are merged with skills.");
table(s, [
  ["Block", "What it is", "RetailCo example"],
  ["CLAUDE.md / rules", "Permanent instructions", "Business pitfalls, conventions"],
  ["Skill", "Reusable procedure, /name or auto-loaded", "/dbt-model, /data-quality-audit"],
  ["Subagent", "Specialist with its own context", "data-reviewer (read-only)"],
  ["Hook", "Shell command, runs deterministically", "ruff format, block secrets"],
  ["MCP", "Standard protocol for external tools", "dbt MCP, Snowflake MCP"],
  ["Plugin", "Package to share skills, agents, hooks", "Future Keyrus Data plugin"],
  ["Headless (claude -p)", "Non-interactive command line", "Nightly quality report"],
], [2.6, 5.0, 4.5], 1.5, 15);

// 19 Rule of thumb
s = N("Which block for which need?", "Rule of thumb. For an external system, MCP or simply its CLI (gh, snow, dbt), often more context-efficient.");
table(s, [
  ["You need...", "Use"],
  ["An instruction to follow most of the time", "CLAUDE.md"],
  ["An occasional multi-step procedure", "Skill"],
  ["A rule that applies 100% of the time", "Hook or deny permission"],
  ["Verbose work, or fresh eyes", "Subagent"],
  ["An external system", "MCP, or simply its CLI (gh, snow, dbt)"],
], [7.0, 5.1], 1.7, 18);

// 20 MCP demo
s = N("Demo: plug in the dbt MCP server",
  "DEMO SCRIPT (6.2). The official dbt Labs MCP server (dbt-mcp) runs locally with uvx and exposes model discovery, lineage and dbt command execution. 1 Run the claude mcp add command, then claude mcp list. 2 In Claude Code run /mcp to see the server status. 3 Ask: 'with the dbt MCP server, list the models that depend on stg_orders and their tests'.");
tag(s, "Demo", K.accent4);
code(s, "claude mcp add dbt \\\n  -e DBT_PROJECT_DIR=\"$PWD/dbt_project\" -e DBT_PATH=\"$(which dbt)\" \\\n  -e DBT_PROFILES_DIR=\"$PWD/dbt_project\" \\\n  -- uvx dbt-mcp\nclaude mcp list", 1.6, 2.2);
code(s, "/mcp   # server status\n> with the dbt MCP server, list the models that depend on stg_orders and their tests", 4.1, 1.3);
callout(s, "dbt-mcp runs locally: model discovery, lineage, dbt commands", 5.8);

// 21 Scopes
s = N("Three installation scopes for an MCP server",
  "local (default, only you, this project); project (committed .mcp.json shared with the team, each member approves the server on first use); user (all your projects). Template: .mcp.json.example; ${VARIABLES} are read from the environment so no secret sits in the file.");
cards(pres, s, [
  { head: "local", body: "Default. Only you, this project" },
  { head: "project", body: "Committed .mcp.json. Shared with the team, each member approves on first use" },
  { head: "user", body: "All your projects" },
], 1.7, 3.8);
callout(s, "Use ${VARIABLES} in .mcp.json: no secret in the file", 5.7);

// 22 Snowflake + caution
s = N("MCP acts with your rights: stay careful",
  "Snowflake offers a managed MCP server (an MCP SERVER object created in the account) exposing Cortex Analyst, Cortex Search, Cortex agents and SQL execution, with Snowflake RBAC. Configure it with a read-only role. Often-sufficient alternative: Claude uses the Snowflake CLI (snow sql -q ...) with a restricted role and an ask rule. Cautions: MCP acts with your rights, never production credentials. Responses enter the context; Claude Code warns above 10,000 tokens of MCP output. Only install servers from known sources (official vendor, Anthropic directory, internal review).");
cards(pres, s, [
  { head: "Least privilege", body: "Test database, read-only role, never production credentials" },
  { head: "Mind the context", body: "Avoid thousands of rows. Warning above 10,000 tokens" },
  { head: "Trusted sources", body: "Official vendor, Anthropic directory, internal review" },
], 1.7, 3.8);
callout(s, "Snowflake: managed MCP server with RBAC, or the snow CLI with a restricted role", 5.7);

// 23 Exercise 3.3
s = N("Plug in dbt-mcp and map tests to columns",
  "Exercise 3.3, 15 min. Prerequisite: uv installed. 1 /mcp: is the server connected, which tools? 2 With MCP, produce the matrix model, tests, untested columns. 3 Compare with the same request without MCP (/mcp to disable): result, number of actions, consumption (/usage).");
tag(s, "Exercise 3.3 | 15 min");
flow(s, [
  { head: "Connect", body: "claude mcp add dbt, then /mcp. Which tools appear?" },
  { head: "Produce", body: "Matrix: model, tests, untested columns" },
  { head: "Compare", body: "Same request without MCP: result, actions, /usage" },
], 1.7, 3.6);
callout(s, "Prerequisite: uv installed", 5.7);

// 24 Skills anatomy
s = N("Anatomy of a skill",
  "SKILLS DEMO (10 min). Open .claude/skills/dbt-model/SKILL.md. Show: the description (it triggers automatic loading); $ARGUMENTS; allowed-tools (tools pre-approved while the skill runs). sql-review: disable-model-invocation: true (only via /sql-review) and the injection of a !`git diff ...` command executed before Claude reads the skill. data-quality-audit: context: fork + agent: Explore runs in a read-only subagent, only the report comes back. Then run /data-quality-audit data/raw/orders.csv and compare with the anomalies found by hand in 3.2.");
tag(s, "Demo | skills", K.accent4);
cards(pres, s, [
  { head: "description", body: "Triggers automatic loading" },
  { head: "$ARGUMENTS and allowed-tools", body: "Inputs, and tools pre-approved while it runs" },
  { head: "disable-model-invocation", body: "sql-review: only via /sql-review" },
  { head: "context: fork", body: "data-quality-audit: read-only subagent, only the report returns" },
], 1.7, 4.6);

// 25 Demo skill run
s = N("Demo: run the audit skill and compare",
  "Run /data-quality-audit data/raw/orders.csv. Compare with the anomalies found by hand in Exercise 3.2.");
tag(s, "Demo | 10 min", K.accent4);
code(s, "/data-quality-audit data/raw/orders.csv", 1.7, 0.9);
flow(s, [
  { head: "Skill loads", body: "Description matched or /name typed" },
  { head: "Forked subagent", body: "Read-only Explore agent does the work" },
  { head: "Report returns", body: "Only the report enters your context" },
], 3.0, 2.6);
callout(s, "Compare with the anomalies you found by hand in 3.2", 5.9);

// 26 Hooks table
s = N("Demo: three hooks guard the project",
  "HOOKS DEMO (10 min). Open .claude/settings.json and the scripts in .claude/hooks/. protect-files.sh: PreToolUse on Edit|Write, blocks writes to .env, data/raw/, .git/, profiles.yml. block-destructive-sql.sh: PreToolUse on Bash, blocks rm -rf, DROP/TRUNCATE TABLE, DELETE without WHERE, dbt on prod. format-python.sh: PostToolUse on Edit|Write, ruff format + ruff check --fix, sends remaining errors back to Claude. Demo: ask 'drop the raw.orders table in DuckDB' -> blocked; Claude explains the block. /hooks lists active hooks.");
tag(s, "Demo | hooks", K.accent4);
table(s, [
  ["Hook", "Event", "Effect"],
  ["protect-files.sh", "PreToolUse on Edit|Write", "Blocks writes to .env, data/raw/, .git/, profiles.yml"],
  ["block-destructive-sql.sh", "PreToolUse on Bash", "Blocks rm -rf, DROP/TRUNCATE, DELETE without WHERE, dbt on prod"],
  ["format-python.sh", "PostToolUse on Edit|Write", "ruff format and check --fix, remaining errors go back to Claude"],
], [3.2, 3.2, 5.7], 1.7, 15);
callout(s, "Try it: \"drop the raw.orders table in DuckDB\" is blocked. /hooks lists active hooks", 5.3, 0.9, K.accent4);

// 27 Hook mechanics
s = N("A hook is a guarantee, CLAUDE.md is a request",
  "Mechanics: the hook receives a JSON description of the action on standard input; exit code 2 = action blocked, and the error message is sent back to Claude, which adapts. Key message: a hook is a guarantee, an instruction in CLAUDE.md is a request.");
flow(s, [
  { head: "Claude acts", body: "About to edit or run a command" },
  { head: "Hook runs", body: "Receives the action as JSON on stdin" },
  { head: "Exit code 2", body: "Action is blocked" },
  { head: "Claude adapts", body: "Gets the error message and tries another way" },
], 1.7, 3.4);
callout(s, "Hook = guarantee. Instruction in CLAUDE.md = request", 5.6);

// 28 Headless
s = N("Automate recurring tasks with claude -p",
  "Non-interactive mode, for scripts, CI or a scheduled task. dontAsk + a tool allowlist = nothing else can run. Consultant use cases: daily quality report, dbt documentation updates, CI failure triage, automatic PR review (HD4).");
code(s, "claude -p \"run /data-quality-audit data/raw/orders.csv and write the report to reports/quality.md\" \\\n  --permission-mode dontAsk \\\n  --allowedTools \"Read\" \"Edit(./reports/**)\" \"Bash(python *)\" \\\n  --output-format json > run.json", 1.6, 1.9);
cards(pres, s, [
  { head: "Daily quality report", body: "Scheduled audit" },
  { head: "dbt docs", body: "Keep documentation updated" },
  { head: "CI triage", body: "Explain failing builds" },
  { head: "PR review", body: "Automatic, covered in HD4" },
], 3.8, 2.8);

// 29 Exercise 3.4
s = N("Build your own automation",
  "Exercise 3.4, 15 min. Choose one. A: skill /explain-model <model> in .claude/skills/explain-model/SKILL.md documenting a dbt model (grain, upstream/downstream lineage, tests, untested columns) and proposing missing tests; test on fct_orders and stg_orders. B: Stop hook in .claude/settings.json running pytest -q at the end of each response and sending failures back (exit code 2); beware of infinite loops: the JSON received contains stop_hook_active. C: non-interactive script scripts/nightly_quality.sh calling claude -p in dontAsk mode with a tool allowlist to produce reports/quality.md.");
tag(s, "Exercise 3.4 | 15 min");
cards(pres, s, [
  { head: "A. A skill", body: "/explain-model <model>: grain, lineage, tests, untested columns. Try it on fct_orders" },
  { head: "B. A Stop hook", body: "Run pytest -q after each response, send failures back. Beware infinite loops: stop_hook_active" },
  { head: "C. A script", body: "nightly_quality.sh calls claude -p in dontAsk mode with an allowlist" },
], 1.7, 4.6);

// 30 Recap
s = N("Recap: three things to remember",
  "1 Test first, business edge cases, review the diff. 2 Data is tested on every load, code on every change. 3 CLAUDE.md = request; hook/permission = guarantee; skill = procedure; MCP = connection; subagent = separate context. Wrap-up is a 20 min discussion.");
cards(pres, s, [
  { head: "Test first", body: "Business edge cases, review the diff" },
  { head: "Two test moments", body: "Data on every load, code on every change" },
  { head: "Pick the right block", body: "CLAUDE.md asks, hook guarantees, skill = procedure, MCP = connection, subagent = fresh context" },
], 1.7, 4.4);

// 31 Closing
darkSlide(pres, "Next: Half-day 4", "Before then: push your fixes branch to the session repository, without merging",
  "For HD4: everyone pushes their fixes branch to the session repository (without merging). Questions and discussion.");

pres.writeFile({ fileName: "half-day-3.pptx" }).then((f) => console.log("wrote", f));
