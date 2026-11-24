# -*- coding: utf-8 -*-
"""Half-day 2 deck, Keyrus template. Run: python slides/build_2.py

STORYBOARD (# | section | message | layout | visual | family)
 1 cover   | Code exploration and Data development       | AI_Cover_Dark
 2 agenda  | 8 blocks, 3 exercises                      | Agenda_8_Items
 3 intro   | /init missed 3 business pitfalls           | TD_Blue_Light   | hub     | blue
 4 sect    | Theme 3                                    | Title_Slide_1 Dark
 5 T3      | First week: 300 models, 2 days             | TD_Blue_Light   | kpis    | blue
 6 T3      | Explore in a funnel                        | TD_Blue_Dark    | funnel  | blue
 7 T3      | Four habits                                | TD_Blue_Light   | cards   | blue
 8 T3      | Demo lineage                               | TD_Blue_Light   | custom  | blue
 9 T3      | Demo riskiest areas, read-only             | TD_Blue_Dark    | custom  | blue
10 T3      | Exercise 2.1                               | TD_Blue_Light   | cards   | blue
11 T3      | Document at three levels                   | TD_Blue_Light   | layers  | blue
12 T3      | Docs describe what code does               | TD_Blue_Light   | versus  | blue
13 sect    | Theme 4                                    | Title_Slide_2 Dark
14 T4      | Five ingredients of a code request         | TD_Yellow_Dark  | hub     | yellow
15 T4      | Snowflake specifics                        | TD_Yellow_Light | table   | yellow
16 T4      | Demo dbt model A to Z                      | TD_Yellow_Light | custom  | yellow
17 T4      | What to narrate                            | TD_Yellow_Light | flow    | yellow
18 break   |                                            | Title_Slide_3 Dark
19 T4      | Exercise 2.2                               | TD_Yellow_Light | kpis+cards | yellow
20 T4      | Exercise 2.2 method                        | TD_Yellow_Light | flow    | yellow
21 T4      | Debrief                                    | TD_Yellow_Light | versus  | yellow
22 sect    | 4.2 Optimise                               | Title_Slide_4 Dark
23 4.2     | Measure, freeze, rewrite, prove            | TD_Red_Dark     | cycle   | red
24 4.2     | The classic trap                           | TD_Red_Light    | custom  | red
25 4.2     | Exercise 2.3: 90 s to < 1 s                | TD_Red_Light    | chart   | red
26 4.2     | Exercise 2.3 method                        | TD_Red_Light    | timeline| red
27 4.2     | Reproduce first                            | TD_Red_Light    | tree    | red
28 recap   | Three rules                                | TD_Blue_Light   | cards   | blue
29 teaser  | Open question for HD3                      | Title_Slide_1 Dark
30 closing | add_closing
Diagram slides: 16 of 22 content slides (73%); text-only slides: 0.
"""
import sys
SKILL = "C:/Users/Stefan.Duprey/.claude/plugins/synced/a8188927-62a2-4df9-9577-7c442b66f830_279e38b6-7f96-4e6c-900a-8904d25cb69d/keyrus-slides~g2/skills/keyrus-slides"
sys.path.insert(0, SKILL + "/scripts")
import kdeck
from diagrams import (add_flow, add_kpis, add_cards, add_timeline, add_cycle, add_funnel,
                      add_layers, add_versus, add_chart, add_hub, add_tree, custom, box, arrow, label)
from insert_table import add_table

prs = kdeck.new_deck()
NAVY = "021E57"


def slide(layout, title, sub, notes):
    s = kdeck.add(prs, layout, title=title, subtitle=sub)
    s.notes_slide.notes_text_frame.text = notes
    return s


def section(layout, title, sub, notes):
    s = kdeck.add(prs, layout, title=title)
    kdeck.fill(s, {20: sub})
    s.notes_slide.notes_text_frame.text = notes
    return s


# 1 Cover
s = kdeck.add(prs, "AI_Cover_Dark", title="Code exploration and Data development",
              subtitle="Half-day 2 - Themes 3 and 4")
s.notes_slide.notes_text_frame.text = (
    "Half-day 2: Understanding an existing codebase and producing Data code. "
    "Themes 3 and 4: Code exploration and AI-assisted Data development. Session length: 4 hours (0:00 to 4:00). "
    "The start time is up to the organiser. All timings in this deck are offsets from the session start.")

# 2 Agenda
s = kdeck.add(prs, "Agenda_8_Items", title="Agenda: 4 hours, 3 exercises")
kdeck.fill(s, {16: "Back to HD1 - 10 min", 17: "3.1 Explore a repository - 25 min",
               18: "Exercise 2.1 Map RetailCo - 35 min", 19: "3.2 Document the code - 15 min",
               20: "4.1 Generate SQL, Python, dbt - 30 min", 21: "Exercise 2.2 Migrate to dbt - 50 min",
               22: "4.2 Optimise + Exercise 2.3 - 50 min", 23: "Wrap-up and HD3 preparation - 10 min"})
s.notes_slide.notes_text_frame.text = (
    "Walk through the plan. Three exercises: 2.1 individual (35 min), 2.2 pairs (50 min), 2.3 individual (35 min). "
    "Detailed offsets: 0:00 Back to HD1 (10 min, discussion); 0:10 3.1 Explore an unfamiliar repository (25 min, talk + demo); "
    "0:35 Exercise 2.1 (35 min); 1:10 3.2 Document the existing code (15 min, demo); "
    "1:25 4.1 Generate and modify SQL / Python / dbt (30 min); 1:55 Break (15 min); 2:10 Exercise 2.2 (50 min, pairs); "
    "3:00 4.2 Optimise existing code (15 min, demo); 3:15 Exercise 2.3 (35 min); 3:50 Wrap-up and HD3 preparation (10 min).")

# 3 Back to HD1
s = slide("Title_Description_Blue_Light", "Back to HD1: what did /init miss?", "Compare with the model CLAUDE.md",
    "Display a volunteer's CLAUDE.md and compare it with the model solution. Ask the room: which business pitfalls did "
    "/init miss? Expected answer: the amount format, multiple versions of orders, split payments. They will come back "
    "later. 10 minutes (0:00).")
add_hub(s, "What /init missed", [("Amount format", "Text, comma decimals, spaces"),
        ("Order versions", "Same order several times in raw files"),
        ("Split payments", "One order paid in instalments")],
        icons=["file-text", "layers", "gauge"], family="blue")

# 4 Section theme 3
section("Title_Slide_1", "Theme 3: Understanding an existing codebase",
      "3.1 Explore an unfamiliar repository and 3.2 Document the existing code",
      "Section opener. 3.1 starts at 0:10, 3.2 at 1:10.")

# 5 Situation
s = slide("Title_Description_Blue_Light", "A consultant's first week on a new engagement",
    "Claude Code reads fast and cross-references",
    "Typical situation: you arrive on an engagement facing a repository with 300 dbt models and 40 Python scripts, no "
    "up-to-date documentation, and 2 days to become operational. Claude Code is particularly strong here: it reads fast, "
    "cross-references files and answers precise questions.")
add_kpis(s, [("300", "dbt models to understand"), ("40", "Python scripts, undocumented"),
             ("2 days", "to become operational")], family="blue")

# 6 Funnel
s = slide("Title_Description_Blue_Dark", "Explore in a funnel: overview to risk areas", "Five questions, each narrower",
    "Funnel approach. 1 Overview: explain the architecture of this repository: layers, data flows, technologies, entry "
    "points. 2 Data flow: trace the path of an order from the raw CSV to fct_orders, file by file. 3 Dependencies: which "
    "Python dependencies are actually imported? Which models depend on stg_orders? 4 Targeted questions: where are "
    "currencies handled? What happens if an amount is empty? 5 Risk areas: which parts look fragile? Cite the lines.")
add_funnel(s, [("Overview", "1", "Layers, flows, entry points"), ("Data flow", "2", "Raw CSV to fct_orders"),
               ("Dependencies", "3", "Who depends on stg_orders?"), ("Targeted", "4", "Currencies? Empty amount?"),
               ("Risk areas", "5", "Fragile code, with lines")], family="blue", dark=True)

# 7 Habits
s = slide("Title_Description_Blue_Light", "Four habits that keep exploration reliable", "Explore, never modify",
    "Stay in Plan Mode or default mode: we explore, we do not modify. Ask for files and line numbers and check 1 or 2 "
    "claims yourself, Claude can be wrong on a detail. For a large repository ask for exploration subagents: the detail "
    "of the reads stays out of the main conversation, only the summary comes back. Use native tools: dbt ls --select "
    "+fct_orders, dbt docs generate (manifest.json contains the full lineage), git log --stat.")
add_cards(s, [("Read-only", "Plan Mode or default mode. Never modify."),
              ("Cite and check", "Ask for files and lines. Verify 1 or 2 claims."),
              ("Subagents", "Parallel reads. Only the summary returns."),
              ("Native tools", "dbt ls, dbt docs generate, git log --stat.")],
          icons=["lock", "check-circle", "network", "settings"], family="blue")

# 8 Demo 1
s = slide("Title_Description_Blue_Light", "Demo: trace the lineage of fct_orders", "Demo, 10 min, two prompts",
    "Demo (10 min, two prompts). Run the prompt live and let the room read the answer. Point out that file names are "
    "cited. Prompt: explain the lineage of fct_orders to me: sources, intermediate models, tests. Use dbt ls and the SQL "
    "files, and cite the files. What to point out: Claude combines dbt ls with the SQL files, and every statement comes "
    "with a file reference.")
with custom(s):
    box(s, 0.7, 3.3, 3.8, 1.9, "Prompt", "Explain the lineage of fct_orders: sources, intermediate models, tests. Cite the files.", family="navy", size=14)
    box(s, 5.6, 2.5, 2.8, 0.9, "dbt ls", family="blue", style="soft")
    box(s, 5.6, 4.9, 2.8, 0.9, "SQL files", family="blue", style="soft")
    box(s, 9.4, 3.3, 3.2, 1.9, "Answer", "Every statement comes with a file reference", family="cyan", size=14)
    arrow(s, 4.5, 3.8, 5.6, 2.95); arrow(s, 4.5, 4.7, 5.6, 5.35)
    arrow(s, 8.4, 2.95, 9.4, 3.8); arrow(s, 8.4, 5.35, 9.4, 4.7)
    label(s, 0.7, 6.1, 12, 0.4, "Point out: Claude combines dbt ls with the SQL files", bold=True, color=NAVY)

# 9 Demo 2
s = slide("Title_Description_Blue_Dark", "Demo: ask for the riskiest areas, read-only", "Demo, one prompt, nothing modified",
    "Depending on the run, Claude often spots the join on payments or the deduplication. DO NOT validate or correct "
    "anything now: say 'we note it, and come back to it in HD3'. The repository has only one commit, so there is no "
    "history to lean on. Prompt: git log contains only one commit, so there is no history: from reading the code alone, "
    "what are the 3 riskiest areas of the project? do not modify anything.")
with custom(s):
    box(s, 0.7, 3.2, 3.6, 2.0, "Prompt", "One commit only. From the code alone: the 3 riskiest areas? Modify nothing.", family="cyan", size=14)
    box(s, 5.3, 3.2, 3.0, 2.0, "Claude, read-only", "Reads code, ranks risks", family="blue", size=14)
    box(s, 9.3, 2.4, 3.3, 0.8, "Risk 1", family="red", style="soft")
    box(s, 9.3, 3.5, 3.3, 0.8, "Risk 2", family="red", style="soft")
    box(s, 9.3, 4.6, 3.3, 0.8, "Risk 3", family="red", style="soft")
    arrow(s, 4.3, 4.2, 5.3, 4.2); arrow(s, 8.3, 4.0, 9.3, 2.8); arrow(s, 8.3, 4.2, 9.3, 3.9); arrow(s, 8.3, 4.4, 9.3, 5.0)
    label(s, 0.7, 5.9, 12, 0.4, "Trainer stance: we note it and come back to it in HD3", bold=True, color="FFFFFF")

# 10 Exercise 2.1
s = slide("Title_Description_Blue_Light", "Exercise 2.1: Map RetailCo", "Individual, 35 min",
    "Individual, 35 min (0:35 to 1:10). Deliverable: docs/ARCHITECTURE.md generated with Claude: Mermaid diagram of the "
    "flow, list of models and their grains, dependencies, open questions section. Success criterion: a newcomer "
    "understands the project after 5 minutes of reading and every claim has been verified (ticked in the document). "
    "Full instructions in exercises/HD2_exploration_development.md.")
add_cards(s, [("Deliverable", "docs/ARCHITECTURE.md: Mermaid flow, models and grains, dependencies, open questions."),
              ("Constraint", "Plan Mode or default mode. Only ARCHITECTURE.md may be written."),
              ("Success", "A newcomer gets it in 5 minutes. Every claim verified and ticked.")],
          icons=["file-text", "lock", "target"], family="blue")

# 11 Doc levels
s = slide("Title_Description_Blue_Light", "Document at three levels, most to least durable",
    "3.2 Document the existing code, demo",
    "3.2 Document the existing code, 15 min demo (1:10). Typical prompts: in the code: add docstrings to the public "
    "functions of transform.py, without changing the code. In dbt: complete the descriptions in _staging.yml from the "
    "SQL and flag what you cannot infer. In the repository: ARCHITECTURE.md, README (Exercise 2.1).")
add_layers(s, [("In the repository", ["ARCHITECTURE.md", "README"]),
               ("In dbt", ["Model descriptions", "Column descriptions in YAML"]),
               ("In the code", ["Docstrings", "Comments on business rules"])], family="blue")

# 12 Doc key message
s = slide("Title_Description_Blue_Light", "Documentation describes what the code does", "Not what it should do",
    "Key message: generated documentation describes what the code does, not what it should do. If the code is wrong (as "
    "it is here), the documentation will faithfully describe the bug. Always ask for an 'assumptions and points to "
    "validate with the business' section.")
add_versus(s, ("Generated documentation", ["Describes what the code does", "If the code is wrong, it describes the bug faithfully"]),
              ("Always ask for", ["A section on assumptions", "Points to validate with the business"]),
           labels=("Key message", "Always ask for"))

# 13 Section theme 4
section("Title_Slide_2", "Theme 4: AI-assisted Data development",
      "4.1 Generate and modify SQL, Python, dbt and 4.2 Optimise existing code",
      "Section opener. 4.1 starts at 1:25, 4.2 at 3:00.")

# 14 Prompt checklist
s = slide("Title_Description_Yellow_Dark", "Five ingredients of a good code request", "Put them in every prompt",
    "Give the dialect and the target: Snowflake SQL, compatible with DuckDB and Snowflake via the project macros. Give "
    "the grain before any query: one row per customer and per month. Give the real names: let Claude read the existing "
    "models rather than describing columns from memory. Require verification: compile with dbt compile, then dbt build "
    "--select model+ and fix until everything passes. Small steps: staging first, mart next, one model at a time.")
add_hub(s, "Good code request", [("Dialect, target", "Snowflake SQL, portable macros"), ("Grain", "One row per customer, month"),
        ("Real names", "Let Claude read the models"), ("Verification", "dbt compile, dbt build model+"),
        ("Small steps", "Staging, then mart")],
        icons=["database", "layers", "file-text", "check-circle", "rocket"], family="yellow", dark=True)

# 15 Snowflake table
s = slide("Title_Description_Yellow_Light", "Snowflake specifics to put in CLAUDE.md", "What to specify in the prompt",
    "Remind people of these specifics and have them appear in CLAUDE.md at the client.")
add_table(s, [["Topic", "What to specify in the prompt"],
    ["Deduplication", "QUALIFY ROW_NUMBER() OVER (...) = 1 (DuckDB supports it too)"],
    ["Tolerant conversion", "TRY_TO_NUMBER, TRY_TO_DATE (Snowflake) vs TRY_CAST (DuckDB): use a macro"],
    ["Semi-structured", "VARIANT, :field::type, LATERAL FLATTEN"],
    ["Incremental", "materialized='incremental', unique_key, merge strategy, is_incremental() filter"],
    ["Cost", "Warehouse size, AUTO_SUSPEND, avoid SELECT * on large tables, query profile"]],
    left=0.7, top=2.1, width=11.9, font_size=13, header_size=13)

# 16 Demo dbt
s = slide("Title_Description_Yellow_Light", "Demo: a dbt model from A to Z", "Demo, 15 min, default mode",
    "Demo (15 min). Live, in default mode so the room sees every action. Comment as it runs: Claude reads stg_orders, "
    "the parse_amount macro and dbt_project.yml; it DISCOVERS that dbt_utils is not installed and adapts; it executes "
    "and fixes. Then show the final diff (git diff): human review is what validates, not 'tests OK'. Prompt: Create a "
    "dbt model marts/fct_daily_sales: one row per day and per channel (channel), with the number of non-cancelled orders "
    "and revenue. Start from stg_orders. Add a uniqueness test on the day+channel combination (singular test or "
    "dbt_utils if available, otherwise singular test), document the grain, then run dbt build --select fct_daily_sales "
    "and fix until everything passes.")
with custom(s):
    box(s, 0.7, 2.3, 6.6, 3.0, "Prompt",
        "Create marts/fct_daily_sales: one row per day and channel, non-cancelled orders and revenue, from stg_orders. "
        "Add a uniqueness test on day + channel, document the grain, run dbt build --select fct_daily_sales, fix until green.",
        family="navy", size=14)
    box(s, 8.2, 2.3, 4.4, 0.8, "dbt build", family="yellow")
    box(s, 8.2, 3.5, 4.4, 0.8, "Errors read and fixed", family="yellow", style="soft")
    box(s, 8.2, 4.7, 4.4, 0.8, "Final git diff", family="blue", style="soft")
    arrow(s, 7.3, 3.8, 8.2, 2.7); arrow(s, 7.3, 3.8, 8.2, 3.9); arrow(s, 7.3, 3.8, 8.2, 5.1)
    label(s, 0.7, 5.9, 12, 0.4, "Run it in default mode: the room sees every file read, command and fix", bold=True, color=NAVY)

# 17 Narrate
s = slide("Title_Description_Yellow_Light", "What to narrate during the demo", "Four moments to comment",
    "Claude reads stg_orders, the parse_amount macro and dbt_project.yml. It discovers that dbt_utils is not installed "
    "and adapts. It executes and fixes. Show the final git diff: it is the human review that validates, not the green tests.")
add_flow(s, [("Reads", "stg_orders, parse_amount macro, dbt_project.yml"), ("Discovers", "dbt_utils is not installed, so it adapts"),
             ("Executes", "dbt build, reads errors, fixes"), ("You review", "git diff: review validates, not 'tests OK'")],
         icons=["file-text", "lightbulb", "settings", "user-check"], family="yellow")

# 18 Break
section("Title_Slide_3", "Break: 15 minutes", "Next: Exercise 2.2 in pairs",
      "Break at 1:55, back at 2:10. Shift as needed. Next: Exercise 2.2 in pairs.")

# 19 Exercise 2.2
s = slide("Title_Description_Yellow_Light", "Exercise 2.2: Migrate a Snowflake query to dbt", "Pairs, 50 min",
    "Pairs, 50 min (2:10 to 3:00). The query sql/legacy/customer_ltv.sql (customer lifetime value, LTV) must become a "
    "model marts/dim_customers.sql. Required approach: explore and list the problems of the query in Plan Mode, validate "
    "the plan in pairs, implement, dbt build, compare the figures with the old logic and explain every discrepancy. For "
    "fast finishers: make fct_orders incremental (merge on order_id, filter on updated_at).")
add_kpis(s, [("2", "people per pair"), ("50 min", "to migrate the query"), ("5", "customers to compare")],
         family="yellow", zone=(0.56, 1.95, 12.2, 2.3))
add_cards(s, [("The task", "sql/legacy/customer_ltv.sql becomes marts/dim_customers.sql."),
              ("Fast finishers", "Make fct_orders incremental: merge on order_id, filter on updated_at.")],
          icons=["database", "rocket"], family="yellow", zone=(0.56, 4.4, 12.2, 2.4))

# 20 Exercise flow
s = slide("Title_Description_Yellow_Light", "Exercise 2.2 method: five steps, validated in pairs",
    "Required approach, in this order",
    "Required approach, in this order. Explore in Plan Mode and list problems (performance, correctness, portability); "
    "plan with grain, reused models, columns, tests; implement portable DuckDB/Snowflake SQL with project macros plus "
    "YAML; verify with cd dbt_project && DBT_PROFILES_DIR=. dbt build --select +dim_customers; compare 5 customers "
    "against the old logic run on DuckDB and explain every discrepancy in the model description.")
add_flow(s, [("Explore", "Plan Mode: list all problems"), ("Plan", "Grain, models, columns, tests"),
             ("Implement", "Portable SQL, YAML with tests"), ("Verify", "dbt build --select +dim_customers"),
             ("Compare", "5 customers vs old logic")],
         icons=["target", "layers", "settings", "check-circle", "gauge"], family="yellow")

# 21 Debrief
s = slide("Title_Description_Yellow_Light", "Debrief: is your dbt build entirely green?", "If not, why is a test still red?",
    "TRAINER NOTES. Problems to bring out: 5 correlated subqueries on the same table; nb_orders includes cancelled "
    "orders while total_revenue excludes them; total_paid inflated by multiple order versions; REPLACE(',', '.') does "
    "not handle '1 234,50'; a useless segment IN (...) filter; non-portable DATEDIFF. DELIBERATE TRAP: most pairs will "
    "build dim_customers on fct_orders, which contains the fan-out bug. Their total_paid will be wrong and the test "
    "unique_fct_orders_order_id stays red. If a pair spots it, congratulate them but we fix it in HD3. If nobody spots "
    "it, ask this question at the debrief. Solution: solutions/dbt_project/models/marts/dim_customers.sql (relies on "
    "the corrected fct_orders).")
add_versus(s, ("Query problems", ["Correlated subqueries", "Inflated totals", "Non-portable functions"]),
              ("Hidden trap", ["Built on fct_orders", "Inherits its fan-out bug", "Fixed in HD3"]),
           labels=("Known issues", "The trap"))

# 22 Section 4.2
section("Title_Slide_4", "4.2 Optimise existing code", "Refactoring with unchanged behaviour",
      "Section opener. Starts at 3:00.")

# 23 Four steps
s = slide("Title_Description_Red_Dark", "Optimising: measure, freeze, rewrite, prove", "A 4-step method to impose on Claude",
    "An optimisation is a refactoring with unchanged behaviour. A 4-step method to impose on Claude. 1 Measure the "
    "existing code (time, memory) and freeze the reference result (CSV file or characterisation test). 2 Diagnose: where "
    "does the time go? (iterrows, filters repeated in a loop, apply(axis=1), N queries instead of one). 3 Rewrite: pandas "
    "vectorisation, joins, or delegate to the SQL engine (DuckDB locally, Snowflake in production). 4 Prove that the "
    "result is identical (automatic comparison) and measure the gain.")
add_cycle(s, [("Measure, freeze", "Time, memory, reference result"), ("Diagnose", "iterrows, apply(axis=1), N queries"),
              ("Rewrite", "Vectorised pandas, DuckDB, Snowflake"), ("Prove", "Identical result, measured gain")],
          center="Same behaviour", family="red", dark=True)

# 24 Trap
s = slide("Title_Description_Red_Light", "The classic trap: numbers change, nobody decided", "A silent behaviour change",
    "The classic trap: the 'optimised' version silently fixes a behaviour of the old one (for example which occurrence "
    "of a duplicated order is used) and the figures change without anyone deciding it. Every divergence must be made "
    "explicit and validated.")
with custom(s):
    box(s, 0.7, 2.5, 3.4, 1.5, "Legacy code", "Keeps one occurrence of a duplicated order", family="navy", size=14)
    box(s, 4.9, 2.5, 3.4, 1.5, "Optimised code", "Silently keeps another occurrence", family="blue", size=14)
    box(s, 9.1, 2.5, 3.5, 1.5, "Figures change", "Nobody decided it", family="red", size=14)
    arrow(s, 4.1, 3.25, 4.9, 3.25); arrow(s, 8.3, 3.25, 9.1, 3.25)
    box(s, 0.7, 4.9, 11.9, 1.1, "The rule", "Every divergence must be made explicit and validated", family="cyan", style="soft", size=14)
    arrow(s, 10.85, 4.0, 10.85, 4.9, dashed=True)

# 25 Exercise 2.3
s = slide("Title_Description_Red_Light", "Exercise 2.3: from 90 s to under one second", "Individual, 35 min, identical result",
    "Individual, 35 min (3:15 to 3:50). src/retail_pipeline/legacy_report.py takes about 90 seconds on the training "
    "dataset. Goal: under one second, strictly identical result, typed and tested code. Warn them: run the old report "
    "only once and save its output, otherwise 90 s are lost on every comparison. A good reflex to have Claude spell out.")
add_chart(s, "hbar", ["legacy_report.py today", "monthly_report.py target"], [("Seconds", [90, 1])],
          family="red", zone=(0.56, 1.95, 12.2, 3.6))
with custom(s):
    label(s, 0.7, 5.9, 12, 0.5, "Warning: run the old report only once and save its output as the reference", bold=True, color="DB0024")

# 26 Exercise 2.3 method
s = slide("Title_Description_Red_Light", "Exercise 2.3 method: reference first, then rewrite", "Five steps to give to Claude",
    "Required method, give it to Claude: run the old report only once and save its output as the reference "
    "(tests/fixtures/monthly_report_reference.csv); diagnose the causes of slowness; rewrite (vectorised pandas or "
    "DuckDB) with typing and docstrings; write a test that compares the new output with the reference; measure the gain.")
add_timeline(s, [("Step 1", "Reference", "Run once, save the CSV"), ("Step 2", "Diagnose", "Causes of slowness"),
                 ("Step 3", "Rewrite", "pandas or DuckDB, typed"), ("Step 4", "Test", "Compare with reference"),
                 ("Step 5", "Measure", "Report the gain")], family="red")

# 27 Subtle point
s = slide("Title_Description_Red_Light", "Reproduce first, fix afterwards, and say so", "Who decides on a legacy behaviour?",
    "Subtle point: the legacy report takes the FIRST occurrence of an order in the file (iloc[0]), not the most recent "
    "one. A 'clean' version that deduplicates on updated_at gives different figures. Good discussion: reproduce first, "
    "fix afterwards, and say so. Solution: solutions/src/retail_pipeline/monthly_report.py (DuckDB, about 0.2 s, zero "
    "difference on the 84 rows).")
add_tree(s, "Duplicated order", [("Legacy behaviour", ["First occurrence (iloc[0])"]),
                                 ("A clean rewrite", ["Dedup on updated_at", "Different figures"]),
                                 ("Right move", ["Reproduce first", "Fix afterwards, say so"])], family="red")

# 28 Recap
s = slide("Title_Description_Blue_Light", "Recap: three rules to take away", "Wrap-up, 10 min",
    "Wrap-up (3:50, 10 min). 1 Explore before producing, ask for sources to be cited, verify. 2 Grain, dialect and "
    "verification criterion in every code request. 3 Optimising is measure, freeze, rewrite, prove.")
add_cards(s, [("Explore first", "Explore before producing. Cite sources. Verify."),
              ("Specify the request", "Grain, dialect and a verification criterion every time."),
              ("Optimise safely", "Measure, freeze, rewrite, prove.")],
          icons=["target", "file-text", "shield-check"], family="blue")

# 29 Teaser
section("Title_Slide_1", "All our tests pass... are our figures right?", "Open question for HD3",
      "Open question for HD3: all our tests pass, but are our figures right? Close the session and point to HD3.")

# 30 Closing
s = kdeck.add_closing(prs, title="Thank you", subtitle="See you in half-day 3")
s.notes_slide.notes_text_frame.text = "Close the session. Next: HD3."

kdeck.save(prs, "c:/Users/Stefan.Duprey/Documents/GitHub/keyrus-claude-code-training/slides/2-code-exploration-data-development.pptx")
print("saved")
