// Half-day 2 deck. Run from slides/: node 2-code-exploration-data-development.js
const { THEME, newDeck, contentSlide, darkSlide, cards, stats } = require("./theme");
const { pres } = newDeck("Half-day 2: Understanding an existing codebase and producing Data code");
const K = THEME.colors;
const SH = pres.ShapeType;

// --- local visual helpers (left-aligned, min 14pt) ---
function code(s, text, y = 1.7, h = 2.6, fontSize = 18) {
  s.addShape(SH.roundRect, { x: 0.6, y, w: 12.1, h, fill: { color: K.dk2 }, line: { color: K.dk2 }, rectRadius: 0.1 });
  s.addText(text, { x: 0.9, y: y + 0.2, w: 11.5, h: h - 0.4, fontFace: "Consolas", fontSize, color: "E2E8F0", valign: "top", align: "left", margin: 0, isTextBox: true });
}
function callout(s, label, text, y = 4.6, h = 1.9, color = K.accent2) {
  s.addShape(SH.roundRect, { x: 0.6, y, w: 12.1, h, fill: { color: K.lt2 }, line: { color: K.lt2 }, rectRadius: 0.1 });
  s.addText(label, { x: 0.9, y: y + 0.2, w: 11.5, h: 0.4, fontSize: 16, bold: true, color, margin: 0, isTextBox: true });
  s.addText(text, { x: 0.9, y: y + 0.65, w: 11.5, h: h - 0.8, fontSize: 20, color: K.dk1, valign: "top", align: "left", margin: 0, isTextBox: true });
}
// horizontal process flow: [{head, body}]
function flow(s, steps, y = 2.0, h = 3.2) {
  const gap = 0.45, w = (12.1 - gap * (steps.length - 1)) / steps.length;
  steps.forEach((st, i) => {
    const x = 0.6 + i * (w + gap);
    s.addShape(SH.roundRect, { x, y, w, h, fill: { color: K.lt2 }, line: { color: K.accent2, width: 1.5 }, rectRadius: 0.1 });
    s.addText(st.head, { x: x + 0.15, y: y + 0.2, w: w - 0.3, h: 0.9, fontSize: 18, bold: true, color: K.dk2, valign: "top", align: "left", margin: 0, isTextBox: true });
    s.addText(st.body, { x: x + 0.15, y: y + 1.15, w: w - 0.3, h: h - 1.3, fontSize: 14, color: K.dk1, valign: "top", align: "left", margin: 0, isTextBox: true });
    if (i < steps.length - 1) s.addShape(SH.rightArrow, { x: x + w + 0.05, y: y + h / 2 - 0.15, w: gap - 0.1, h: 0.3, fill: { color: K.accent2 }, line: { color: K.accent2 } });
  });
}
function table(s, header, rows, colW, y = 1.7, fontSize = 15) {
  const hdr = header.map(t => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: K.dk2 }, fontSize, align: "left" } }));
  const body = rows.map((r, i) => r.map(t => ({ text: t, options: { fontSize, color: K.dk1, align: "left", valign: "middle", fill: { color: i % 2 ? "FFFFFF" : K.lt2 } } })));
  s.addTable([hdr, ...body], { x: 0.6, y, w: 12.1, colW, border: { type: "solid", pt: 0.5, color: "CBD5E1" }, margin: 0.08 });
}
// tag chip for exercises / demos
function tag(s, text, color = K.accent2) {
  s.addText(text, { x: 9.7, y: 1.15, w: 3.0, h: 0.4, shape: SH.roundRect, rectRadius: 0.1, fill: { color }, color: "FFFFFF", bold: true, fontSize: 16, align: "center", valign: "middle", margin: 0, isTextBox: true });
}

// 1 Title
darkSlide(pres, "Half-day 2: Understanding an existing codebase and producing Data code",
  "Themes 3 and 4: Code exploration and AI-assisted Data development",
  "Session length: 4 hours (0:00 to 4:00). The start time is up to the organiser (e.g. 09:00 or 13:30). All timings in this deck are offsets from the session start.");

// 2 Agenda
let s = contentSlide(pres, "Agenda: 4 hours, 3 exercises", "Walk through the plan. Three exercises: 2.1 individual (35 min), 2.2 pairs (50 min), 2.3 individual (35 min). The break is at 1:55.");
table(s, ["Offset", "Min", "Sequence", "Format"], [
  ["0:00", "10", "Back to HD1: a CLAUDE.md on screen", "Discussion"],
  ["0:10", "25", "3.1 Explore an unfamiliar repository", "Talk + demo"],
  ["0:35", "35", "Exercise 2.1: Map RetailCo", "Individual"],
  ["1:10", "15", "3.2 Document the existing code", "Demo"],
  ["1:25", "30", "4.1 Generate and modify SQL / Python / dbt", "Talk + demo"],
  ["1:55", "15", "Break", ""],
  ["2:10", "50", "Exercise 2.2: Migrate a Snowflake query to dbt", "Pairs"],
  ["3:00", "15", "4.2 Optimise existing code", "Demo"],
  ["3:15", "35", "Exercise 2.3: Optimise the legacy report", "Individual"],
  ["3:50", "10", "Wrap-up and HD3 preparation", "Discussion"],
], [1.3, 0.9, 7.2, 2.7], 1.5, 15);

// 3 Back to HD1
s = contentSlide(pres, "Back to HD1: what did /init miss? (0:00)", "Display a volunteer's CLAUDE.md and compare it with the model solution. Ask the room: which business pitfalls did /init miss? Expected answer: the amount format, multiple versions of orders, split payments. They will come back later. 10 minutes.");
cards(pres, s, [
  { head: "Amount format", body: "Amounts are stored as text with comma decimals and spaces." },
  { head: "Order versions", body: "The same order can appear several times in the raw files." },
  { head: "Split payments", body: "One order can be paid in several instalments." },
], 1.7, 4.4);

// 4 Section theme 3
darkSlide(pres, "Theme 3: Understanding an existing codebase", "3.1 Explore an unfamiliar repository (0:10) and 3.2 Document the existing code (1:10)", "Section opener.");

// 5 Situation
s = contentSlide(pres, "The consultant's first week on a new engagement", "Typical situation: you arrive on an engagement facing a repository with 300 dbt models and 40 Python scripts, no up-to-date documentation, and 2 days to become operational. Claude Code is particularly strong here: it reads fast, cross-references files and answers precise questions.");
stats(pres, s, [
  { value: "300", label: "dbt models to understand" },
  { value: "40", label: "Python scripts, undocumented" },
  { value: "2 days", label: "to become operational" },
], 1.9);
callout(s, "Claude Code's strength", "It reads fast, cross-references files and answers precise questions.", 5.0, 1.5);

// 6 Funnel
s = contentSlide(pres, "Explore in a funnel: from overview to risk areas", "Funnel approach. 1 Overview: explain the architecture of this repository: layers, data flows, technologies, entry points. 2 Data flow: trace the path of an order from the raw CSV to fct_orders, file by file. 3 Dependencies: which Python dependencies are actually imported? Which models depend on stg_orders? 4 Targeted questions: where are currencies handled? What happens if an amount is empty? 5 Risk areas: which parts look fragile? Cite the lines.");
flow(s, [
  { head: "1. Overview", body: "Layers, flows, technologies, entry points" },
  { head: "2. Data flow", body: "Raw CSV to fct_orders, file by file" },
  { head: "3. Dependencies", body: "Imported vs declared; who depends on stg_orders?" },
  { head: "4. Targeted", body: "Where are currencies handled? Empty amount?" },
  { head: "5. Risk areas", body: "Fragile or inconsistent code, with lines" },
], 1.9, 3.6);

// 7 Good practices
s = contentSlide(pres, "Four habits that keep exploration reliable", "Stay in Plan Mode or default mode: we explore, we do not modify. Ask for files and line numbers and check 1 or 2 claims yourself, Claude can be wrong on a detail. For a large repository ask for exploration subagents: the detail of the reads stays out of the main conversation, only the summary comes back. Use native tools: dbt ls --select +fct_orders, dbt docs generate (manifest.json contains the full lineage), git log --stat.");
cards(pres, s, [
  { head: "Read-only", body: "Plan Mode or default mode. Explore, never modify." },
  { head: "Cite and check", body: "Ask for files and lines; verify 1 or 2 claims yourself." },
  { head: "Subagents", body: "Parallel exploration; only the summary returns." },
  { head: "Native tools", body: "dbt ls, dbt docs generate, git log --stat." },
], 1.7, 4.4);

// 8 Demo 1
s = contentSlide(pres, "Demo: trace the lineage of fct_orders", "Demo (10 min, two prompts). Run the prompt live and let the room read the answer. Point out that file names are cited.");
tag(s, "DEMO 10 min", K.accent3);
code(s, "explain the lineage of fct_orders to me: sources,\nintermediate models, tests. Use dbt ls and the SQL\nfiles, and cite the files.", 1.7, 2.2, 22);
callout(s, "What to point out", "Claude combines dbt ls with the SQL files, and every statement comes with a file reference.", 4.3, 1.9);

// 9 Demo 2
s = contentSlide(pres, "Demo: ask for the riskiest areas, read-only", "Depending on the run, Claude often spots the join on payments or the deduplication. DO NOT validate or correct anything now: say 'we note it, and come back to it in HD3'. The repository has only one commit, so there is no history to lean on.");
tag(s, "DEMO", K.accent3);
code(s, "git log contains only one commit, so there is no history:\nfrom reading the code alone, what are the 3 riskiest\nareas of the project? do not modify anything.", 1.7, 2.2, 22);
callout(s, "Trainer stance", "Do not validate or correct anything now. We note it and come back to it in HD3.", 4.3, 1.9, K.accent6);

// 10 Exercise 2.1
s = contentSlide(pres, "Exercise 2.1: Map RetailCo", "Individual, 35 min (0:35 to 1:10). Deliverable: docs/ARCHITECTURE.md generated with Claude: Mermaid diagram of the flow, list of models and their grains, dependencies, open questions section. Success criterion: a newcomer understands the project after 5 minutes of reading and every claim has been verified (ticked in the document). Full instructions in exercises/HD2_exploration_development.md.");
tag(s, "EXERCISE 2.1 | 35 min");
cards(pres, s, [
  { head: "Deliverable", body: "docs/ARCHITECTURE.md with a Mermaid flow, models and grains, dependencies, open questions." },
  { head: "Constraint", body: "Plan Mode or default mode. Only ARCHITECTURE.md may be written." },
  { head: "Success", body: "A newcomer gets it in 5 minutes. Every claim is verified and ticked." },
], 1.7, 4.4);

// 11 Doc levels
s = contentSlide(pres, "Document at three levels, from most to least durable", "3.2 Document the existing code, 15 min demo (1:10). Typical prompts: add docstrings to the public functions of transform.py without changing the code; complete the descriptions in _staging.yml from the SQL and flag what you cannot infer.");
table(s, ["Level", "Example", "Typical prompt"], [
  ["In the code", "Docstrings, comments on business rules", "Add docstrings to the public functions of transform.py, without changing the code"],
  ["In dbt", "Model and column descriptions in YAML", "Complete the descriptions in _staging.yml from the SQL; flag what you cannot infer"],
  ["In the repository", "ARCHITECTURE.md, README", "(Exercise 2.1)"],
], [2.3, 4.0, 5.8], 1.9, 16);

// 12 Doc key message
s = contentSlide(pres, "Documentation describes what the code does", "Key message: generated documentation describes what the code does, not what it should do. If the code is wrong (as it is here), the documentation will faithfully describe the bug. Always ask for an 'assumptions and points to validate with the business' section.");
callout(s, "KEY MESSAGE", "Generated documentation describes what the code does, not what it should do. If the code is wrong, the documentation will faithfully describe the bug.", 1.8, 2.4);
callout(s, "ALWAYS ASK FOR", "A section on assumptions and points to validate with the business.", 4.5, 1.7, K.accent3);

// 13 Section theme 4
darkSlide(pres, "Theme 4: AI-assisted Data development", "4.1 Generate and modify SQL / Python / dbt (1:25) and 4.2 Optimise existing code (3:00)", "Section opener.");

// 14 Prompt checklist
s = contentSlide(pres, "Five ingredients of a good code request", "Give the dialect and the target: Snowflake SQL, compatible with DuckDB and Snowflake via the project macros. Give the grain before any query: one row per customer and per month. Give the real names: let Claude read the existing models rather than describing columns from memory. Require verification: compile with dbt compile, then dbt build --select model+ and fix until everything passes. Small steps: staging first, mart next, one model at a time.");
cards(pres, s, [
  { head: "Dialect and target", body: "Snowflake SQL; portable via project macros." },
  { head: "Grain", body: "One row per customer and per month." },
  { head: "Real names", body: "Let Claude read the existing models." },
  { head: "Verification", body: "dbt compile, then dbt build --select model+." },
  { head: "Small steps", body: "Staging first, then mart. One model at a time." },
], 1.7, 4.6);

// 15 Snowflake table
s = contentSlide(pres, "Snowflake specifics to put in CLAUDE.md", "Remind people of these specifics and have them appear in CLAUDE.md at the client.");
table(s, ["Topic", "What to specify in the prompt"], [
  ["Deduplication", "QUALIFY ROW_NUMBER() OVER (...) = 1 (DuckDB supports it too)"],
  ["Tolerant conversion", "TRY_TO_NUMBER, TRY_TO_DATE (Snowflake) vs TRY_CAST (DuckDB): use a macro"],
  ["Semi-structured", "VARIANT, :field::type, LATERAL FLATTEN"],
  ["Incremental", "materialized='incremental', unique_key, incremental_strategy='merge', is_incremental() filter"],
  ["Cost", "Warehouse size, AUTO_SUSPEND, avoid SELECT * on large tables, query profile"],
], [3.0, 9.1], 1.7, 16);

// 16 Demo dbt
s = contentSlide(pres, "Demo: a dbt model from A to Z", "Demo (15 min). Live, in default mode so the room sees every action. Comment as it runs: Claude reads stg_orders, the parse_amount macro and dbt_project.yml; it DISCOVERS that dbt_utils is not installed and adapts; it executes and fixes. Then show the final diff (git diff): human review is what validates, not 'tests OK'.");
tag(s, "DEMO 15 min", K.accent3);
code(s, "Create a dbt model marts/fct_daily_sales: one row per day and\nper channel (channel), with the number of non-cancelled orders\nand revenue. Start from stg_orders. Add a uniqueness test on\nthe day+channel combination (singular test or dbt_utils if\navailable, otherwise singular test), document the grain, then\nrun dbt build --select fct_daily_sales and fix until\neverything passes.", 1.75, 3.4, 18);
callout(s, "Run it in default mode", "The room sees every file read, every command and every fix.", 5.3, 1.3);

// 17 What to commentate
s = contentSlide(pres, "What to narrate during the demo", "Claude reads stg_orders, the parse_amount macro and dbt_project.yml. It discovers that dbt_utils is not installed and adapts. It executes and fixes. Show the final git diff: it is the human review that validates, not the green tests.");
flow(s, [
  { head: "Reads", body: "stg_orders, the parse_amount macro, dbt_project.yml" },
  { head: "Discovers", body: "dbt_utils is not installed, so it adapts" },
  { head: "Executes", body: "dbt build, reads errors, fixes" },
  { head: "You review", body: "git diff: human review validates, not 'tests OK'" },
], 1.9, 3.4);

// 18 Break
darkSlide(pres, "Break: 15 minutes", "From 1:55 to 2:10. Next: Exercise 2.2 in pairs.", "Break. Shift as needed.");

// 19 Exercise 2.2
s = contentSlide(pres, "Exercise 2.2: Migrate a Snowflake query to dbt", "Pairs, 50 min (2:10 to 3:00). The query sql/legacy/customer_ltv.sql (customer lifetime value, LTV) must become a model marts/dim_customers.sql. Required approach: explore and list the problems of the query in Plan Mode, validate the plan in pairs, implement, dbt build, compare the figures with the old logic and explain every discrepancy. For fast finishers: make fct_orders incremental (merge on order_id, filter on updated_at).");
tag(s, "EXERCISE 2.2 | 50 min");
stats(pres, s, [
  { value: "2", label: "people per pair" },
  { value: "50 min", label: "sql/legacy/customer_ltv.sql becomes marts/dim_customers.sql" },
  { value: "5", label: "customers to compare against the old logic" },
], 1.7);
callout(s, "Fast finishers", "Make fct_orders incremental: merge on order_id, filtered on updated_at.", 5.0, 1.5, K.accent4);

// 20 Exercise flow
s = contentSlide(pres, "Exercise 2.2 method: five steps, validated in pairs", "Required approach, in this order. Explore in Plan Mode and list problems (performance, correctness, portability); plan with grain, reused models, columns, tests; implement portable DuckDB/Snowflake SQL with project macros plus YAML; verify with cd dbt_project && DBT_PROFILES_DIR=. dbt build --select +dim_customers; compare 5 customers against the old logic run on DuckDB and explain every discrepancy in the model description.");
flow(s, [
  { head: "1. Explore", body: "Plan Mode: list all problems of the query" },
  { head: "2. Plan", body: "Grain, models, columns, tests. Validate in pairs" },
  { head: "3. Implement", body: "Portable SQL, YAML with tests" },
  { head: "4. Verify", body: "dbt build --select +dim_customers" },
  { head: "5. Compare", body: "5 customers vs old logic. Explain each gap" },
], 1.9, 3.6);

// 21 Debrief
s = contentSlide(pres, "Debrief: is your dbt build entirely green?", "TRAINER NOTES. Problems to bring out: 5 correlated subqueries on the same table; nb_orders includes cancelled orders while total_revenue excludes them; total_paid inflated by multiple order versions; REPLACE(',', '.') does not handle '1 234,50'; a useless segment IN (...) filter; non-portable DATEDIFF. DELIBERATE TRAP: most pairs will build dim_customers on fct_orders, which contains the fan-out bug. Their total_paid will be wrong and the test unique_fct_orders_order_id stays red. If a pair spots it, congratulate them but we fix it in HD3. If nobody spots it, ask this question at the debrief. Solution: solutions/dbt_project/models/marts/dim_customers.sql (relies on the corrected fct_orders).");
callout(s, "QUESTION FOR THE ROOM", "Is your full dbt build entirely green? If not, why is a test still red?", 1.8, 2.0, K.accent6);
cards(pres, s, [
  { head: "Query problems", body: "Correlated subqueries, inflated totals, non-portable functions." },
  { head: "Hidden trap", body: "Building on fct_orders inherits its fan-out bug. Fixed in HD3." },
], 4.1, 2.5);

// 22 Section 4.2
darkSlide(pres, "4.2 Optimise existing code", "Refactoring with unchanged behaviour (3:00)", "Section opener.");

// 23 Four steps
s = contentSlide(pres, "Optimising: measure, freeze, rewrite, prove", "An optimisation is a refactoring with unchanged behaviour. A 4-step method to impose on Claude. 1 Measure the existing code (time, memory) and freeze the reference result (CSV file or characterisation test). 2 Diagnose: where does the time go? (iterrows, filters repeated in a loop, apply(axis=1), N queries instead of one). 3 Rewrite: pandas vectorisation, joins, or delegate to the SQL engine (DuckDB locally, Snowflake in production). 4 Prove that the result is identical (automatic comparison) and measure the gain.");
flow(s, [
  { head: "1. Measure and freeze", body: "Time, memory. Save the reference result (CSV or characterisation test)" },
  { head: "2. Diagnose", body: "iterrows, repeated filters, apply(axis=1), N queries" },
  { head: "3. Rewrite", body: "Vectorised pandas, joins, or DuckDB / Snowflake" },
  { head: "4. Prove", body: "Automatic comparison, then measure the gain" },
], 1.9, 3.6);

// 24 Trap
s = contentSlide(pres, "The classic trap: numbers change and nobody decided", "The classic trap: the 'optimised' version silently fixes a behaviour of the old one (for example which occurrence of a duplicated order is used) and the figures change without anyone deciding it. Every divergence must be made explicit and validated.");
callout(s, "THE TRAP", "The optimised version silently changes a behaviour, such as which occurrence of a duplicated order is used. The figures change without anyone deciding it.", 1.8, 2.3, K.accent6);
callout(s, "THE RULE", "Every divergence must be made explicit and validated.", 4.4, 1.6);

// 25 Exercise 2.3
s = contentSlide(pres, "Exercise 2.3: Optimise the legacy report", "Individual, 35 min (3:15 to 3:50). src/retail_pipeline/legacy_report.py takes about 90 seconds on the training dataset. Goal: under one second, strictly identical result, typed and tested code. Warn them: run the old report only once and save its output, otherwise 90 s are lost on every comparison. A good reflex to have Claude spell out.");
tag(s, "EXERCISE 2.3 | 35 min");
stats(pres, s, [
  { value: "90 s", label: "legacy_report.py today" },
  { value: "< 1 s", label: "target for monthly_report.py" },
  { value: "100%", label: "identical result, typed and tested" },
], 1.9);
callout(s, "Warning", "Run the old report only once and save its output as the reference.", 5.0, 1.5, K.accent3);

// 26 Exercise 2.3 method
s = contentSlide(pres, "Exercise 2.3 method: reference first, then rewrite", "Required method, give it to Claude: run the old report only once and save its output as the reference (tests/fixtures/monthly_report_reference.csv); diagnose the causes of slowness; rewrite (vectorised pandas or DuckDB) with typing and docstrings; write a test that compares the new output with the reference; measure the gain.");
flow(s, [
  { head: "1. Reference", body: "Run once, save monthly_report_reference.csv" },
  { head: "2. Diagnose", body: "Causes of slowness" },
  { head: "3. Rewrite", body: "pandas or DuckDB, typed, with docstrings" },
  { head: "4. Test", body: "Compare new output with the reference" },
  { head: "5. Measure", body: "Report the gain" },
], 1.9, 3.4);

// 27 Subtle point
s = contentSlide(pres, "Reproduce first, fix afterwards, and say so", "Subtle point: the legacy report takes the FIRST occurrence of an order in the file (iloc[0]), not the most recent one. A 'clean' version that deduplicates on updated_at gives different figures. Good discussion: reproduce first, fix afterwards, and say so. Solution: solutions/src/retail_pipeline/monthly_report.py (DuckDB, about 0.2 s, zero difference on the 84 rows).");
cards(pres, s, [
  { head: "Legacy behaviour", body: "Takes the first occurrence of an order in the file (iloc[0])." },
  { head: "A 'clean' rewrite", body: "Deduplicates on updated_at and gives different figures." },
  { head: "Who decides?", body: "Reproduce first, fix afterwards, and say so." },
], 1.7, 4.4);

// 28 Recap
s = contentSlide(pres, "Recap: three rules to take away", "Wrap-up (3:50, 10 min). 1 Explore before producing, ask for sources to be cited, verify. 2 Grain, dialect and verification criterion in every code request. 3 Optimising is measure, freeze, rewrite, prove.");
cards(pres, s, [
  { head: "Explore first", body: "Explore before producing. Cite sources. Verify." },
  { head: "Specify the request", body: "Grain, dialect and a verification criterion every time." },
  { head: "Optimise safely", body: "Measure, freeze, rewrite, prove." },
], 1.7, 4.4);

// 29 Closing
darkSlide(pres, "All our tests pass... are our figures right?", "Open question for HD3 (3:50)", "Open question for HD3: all our tests pass, but are our figures right? Close the session and point to HD3.");

pres.writeFile({ fileName: "2-code-exploration-data-development.pptx" }).then(f => console.log("wrote", f));
