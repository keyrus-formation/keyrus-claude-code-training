# -*- coding: utf-8 -*-
"""Half-day 3 deck (Testing, Quality & Integrations) rebuilt with the Keyrus template.
Run: python slides/build_3.py   (writes slides/3-testing-quality-integrations.pptx)

STORYBOARD  (section colours: Theme 5 = Blue, Theme 6 = Yellow, recap = Red)
 #  section  title-message                          layout                      visual form
 1  -        Cover                                  AI_Cover_Dark               -
 2  -        Agenda                                 Agenda_8_Items              agenda
 3  T5       Section opener Theme 5                 Title_Slide_1 (Dark)        -
 4  T5       Green suite only proves what it tests  Title_Description_Blue      kpis
 5  T5       Five ground rules                      Title_Description_Blue      cards
 6  T5       Test first (TDD loop)                  Title_Description_Blue      flow
 7  T5       Debugging in 4 steps                   Title_Description_Blue      cycle
 8  T5       Raw material, never paraphrase         Title_Description_Blue      versus
 9  T5       Ex 3.1 revenue vs accounting           Title_Description_Blue      hub
10  T5       Debrief: four bugs                     Title_Description_Blue      table
11  T5       Debrief: rows affected                 Title_Description_Blue      chart (hbar)
12  T5       Two kinds of tests                     Title_Description_Blue      versus
13  T5       Flag source anomalies                  Title_Description_Blue      kpis
14  T5       5-point checklist                      Title_Description_Blue      flow
15  T5       Ex 3.2 quality checks                  Title_Description_Blue      flow
16  -        Break                                  Title_Slide_3 (Dark)        -
17  T6       Section opener Theme 6                 Title_Slide_2 (Dark)        -
18  T6       Toolbox: seven blocks                  Title_Description_Yellow    hub
19  T6       Which block for which need             Title_Description_Yellow    table
20  T6       Demo dbt MCP                           Title_Description_Yellow    custom
21  T6       Three MCP scopes                       Title_Description_Yellow    layers
22  T6       MCP acts with your rights              3_Text_Boxes                text boxes + icons
23  T6       Ex 3.3 dbt-mcp                         Title_Description_Yellow    flow
24  T6       Anatomy of a skill                     Title_Description_Yellow    tree
25  T6       Demo run the audit skill               Title_Description_Yellow    custom + flow
26  T6       Demo three hooks                       Title_Description_Yellow    table
27  T6       Hook = guarantee                       Title_Description_Yellow    flow
28  T6       claude -p                              Title_Description_Yellow    custom
29  T6       Ex 3.4 automation                      3_Text_Boxes                text boxes + icons
30  recap    Recap                                  Title_Description_Red       cards
31  -        Next: Half-day 4                       Title_Slide_4 (Dark)        -
32  -        Closing                                AI_Cover_Dark (add_closing) -
Native diagrams: 16 of 25 content slides (64%).
"""
import sys
import os

SKILL = ("C:/Users/Stefan.Duprey/.claude/plugins/synced/a8188927-62a2-4df9-9577-7c442b66f830_"
         "279e38b6-7f96-4e6c-900a-8904d25cb69d/keyrus-slides~g2/skills/keyrus-slides")
sys.path.insert(0, SKILL + "/scripts")
import kdeck
from diagrams import (add_flow, add_kpis, add_cards, add_cycle, add_layers, add_versus,
                      add_chart, add_hub, add_tree, custom, box, arrow, label)
from insert_icons import add_icons
from insert_table import add_table
from pptx.util import Pt
from pptx.enum.shapes import PP_PLACEHOLDER


def icons(s, names):
    """add_icons, then drop the now-redundant empty icon placeholders (QA flags them)."""
    add_icons(s, names)
    for ph in list(s.placeholders):
        if ph.placeholder_format.type == PP_PLACEHOLDER.BITMAP:
            ph._element.getparent().remove(ph._element)

prs = kdeck.new_deck()
B, Y, R = "Blue", "Yellow", "Red"


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text
    return s


def content(color, title, sub, nt, layout="Title_Description_{}_Light"):
    s = kdeck.add(prs, layout.format(color), title=title, subtitle=sub)
    return notes(s, nt)


def section(layout, title, sub, nt):
    s = kdeck.add(prs, layout, title=title)
    kdeck.fill(s, {20: sub})
    return notes(s, nt)


def code(s, x, y, w, h, text, size=11):
    sp = box(s, x, y, w, h, family="navy", style="solid", shape="rect")
    tf = sp.text_frame
    tf.word_wrap = True
    lines = text.split("\n")
    tf.text = lines[0]
    for ln in lines[1:]:
        tf.add_paragraph().text = ln
    from pptx.enum.text import PP_ALIGN
    for p in tf.paragraphs:
        p.alignment = PP_ALIGN.LEFT
        for r in p.runs:
            r.font.name = "Consolas"
            r.font.size = Pt(size)
    return sp


# 1 Cover
s = kdeck.add(prs, "AI_Cover_Dark", title="Half-day 3: Make it reliable and equip it",
              subtitle="Testing, debugging and quality, then integrations and automation with Claude Code")
notes(s, "Session start time is up to the organiser. 4-hour session, timings are offsets from the start.")

# 2 Agenda
s = kdeck.add(prs, "Agenda_8_Items", title="Agenda: 4 hours, two themes")
kdeck.fill(s, {16: "5.1 Testing with an agent - 20 min", 17: "Exercise 3.1: the 4-bug hunt - 55 min",
               18: "5.2 Data quality + Exercise 3.2 - 40 min", 19: "Break - 15 min",
               20: "6.1 The toolbox - 25 min", 21: "6.2 MCP + Exercise 3.3 - 25 min",
               22: "6.3 Skills, hooks + Exercise 3.4 - 40 min", 23: "Wrap-up and HD4 prep - 20 min"})
notes(s, "Theme 5: Testing, debugging & quality. Theme 6: Integrations and automation. "
         "Timings: 5.1 talk 20 min, Exercise 3.1 55 min, 5.2 talk 15 min, Exercise 3.2 25 min, break 15 min, "
         "6.1 talk 25 min, 6.2 MCP demo plus Exercise 3.3 25 min, 6.3 skills, hooks, automation plus Exercise 3.4 40 min, "
         "wrap-up and preparation for HD4 20 min. The break is a break: let people stretch and refill coffee.")

# 3 Section 5
section("Title_Slide_1", "Theme 5: Testing, debugging and quality", "First part of the half-day",
        "Section opener. 5.1 (20 min talk), Exercise 3.1 (55 min), 5.2 (15 min talk), Exercise 3.2 (25 min).")

# 4 Green suite
s = content(B, "A green test suite only proves what it tests",
            "An agent that writes code and its tests can validate its own mistakes",
            "Recall the question left at the end of HD2: the 4 Python tests pass, and yet the pipeline loses money. "
            "An agent that writes code AND its tests can write tests that validate its own mistakes.")
add_kpis(s, [("4 / 4", "unit tests pass", "on the training pipeline"),
             ("4", "bugs hidden", "in the pipeline and the dbt model"),
             ("?", "who checks the tests", "that the tests themselves are right")], family="blue")

# 5 Five rules
s = content(B, "Five ground rules with Claude Code", "How to keep the agent honest",
            "1 TDD: a test that has never failed has proven nothing. 2 Edge cases come from you: French formats, empty values, "
            "duplicates, currencies, time zones, split payments. 3 Put in CLAUDE.md: 'never modify an existing test to make it pass; "
            "flag it instead'. 4 Forbid try/except: pass, silent errors=\"coerce\", DISTINCT that hides a wrong join. "
            "5 Human review is the last line of defence; for fresh eyes use the data-reviewer subagent.")
add_cards(s, [("Test first", "Show the test failing, then fix"),
              ("Your edge cases", "Formats, blanks, duplicates, FX"),
              ("Tests stay put", "Never edit a test to pass it"),
              ("No workarounds", "No bare except, no masking DISTINCT"),
              ("Review the diff", "Human, or the data-reviewer subagent")],
          icons=["check-circle", "lightbulb", "lock", "shield-check", "user-check"], family="blue")

# 6 TDD loop
s = content(B, "Test first: a test that never failed proves nothing",
            "Prompt: write a test that reproduces the bug, show me it fails, then fix it",
            "Prompt: 'write a test that reproduces the bug, show me it fails, then fix it'.")
add_flow(s, [("Write the test", "Reproduces the bug on the current code"),
             ("See it fail", "Red proves the test can catch the bug"),
             ("Fix the cause", "Smallest change, no unrelated edits"),
             ("See it pass", "Whole suite green, impact quantified")],
         icons=["file-text", "target", "settings", "check-circle"], family="blue")

# 7 Debugging 4 steps
s = content(B, "Debugging in 4 steps", "Reproduce, locate, fix, prove",
            "Reproduce: 'here is the symptom: ... write the smallest script or test that reproduces it'. Locate: 'find the root cause, "
            "not the symptom; explain it before proposing a fix'. Fix: 'fix only the cause, without unrelated changes'. "
            "Prove: 'the reproduction test passes, the whole suite passes, and here is the quantified impact on the data'.")
add_cycle(s, [("1 Reproduce", "Smallest script or test"), ("2 Locate", "Root cause, not symptom"),
              ("3 Fix", "Only the cause"), ("4 Prove", "Suite green, impact in numbers")],
          center="Debug loop", family="blue")

# 8 Raw material
s = content(B, "Give Claude the raw material, never a paraphrase", "Better input gives a better root cause",
            "Provide the full error message, the dbt build output, a sample of rows. Do not paraphrase.")
add_versus(s, ("Do paste", ["Full error message and stack trace", "Output of dbt build", "A sample of real rows"]),
           ("Do not paste", ["Your summary of the error", "\"It fails on the join\"", "A guess presented as a fact"]),
           labels=("Do", "Do not"))

# 9 Exercise 3.1
s = content(B, "The business says: revenue does not match accounting",
            "Exercise 3.1 (55 min): for each bug a failing test, the fix, the quantified impact. No edited tests, no DISTINCT, no swallowed exceptions",
            "Exercise 3.1, 55 min, individual then group debrief (10 min). Participants have Claude Code, the red dbt build and their CLAUDE.md. "
            "For each bug: a failing test, the fix, the quantified impact. Rules: no editing a test to pass it, no DISTINCT to hide a duplicate, "
            "no swallowed exception. TRAINER SHEET (do not hand out): B1 transform.parse_amount: '1 234,50' keeps the thousands space, "
            "ValueError swallowed, None: 366 orders without amount, about 572k EUR ignored. B2 transform.clean_orders: ascending sort + keep='first' "
            "keeps the OLDEST version: 1,000 orders with stale status, return rate underestimated. B3 clean_orders: divides by the rate instead of "
            "multiplying (FX_TO_EUR = value of one unit in EUR): 4,058 USD/CHF orders wrong, 100 USD gives 108.70 instead of 92. "
            "B4 fct_orders.sql and build_order_facts: direct join on payments (2 payments for some orders), fan-out: 2,796 duplicate rows, "
            "revenue inflated by about 901k EUR, dbt test unique_fct_orders_order_id fails. HINTS every 15 min: 1 compare count(*) and "
            "count(distinct order_id) in fct_orders. 2 how many non-empty amounts become None after parse_amount? 3 take an order present twice "
            "in orders.csv: which status does the pipeline keep? 4 100 USD is how many euros?")
add_hub(s, "Revenue does not match accounting",
        [("Revenue too high", "fct_orders is above accounting"), ("Large B2B orders", "Some show no amount"),
         ("Odd dollar amounts", "USD conversions look wrong"), ("Return rate too low", "Customer service sees more")],
        icons=["trending-up", "file-text", "chart-bar", "gauge"], family="blue")

# 10 Debrief table
s = content(B, "Debrief: four bugs, real money", "Where they hide and what they cost",
            "Debrief 10 min. How many bugs found? Which did Claude find spontaneously, which thanks to a business question? Usually B4 is found "
            "quickly thanks to the red dbt test; B1 and B3 thanks to the CLAUDE.md enriched in HD1; B2 is the one most often missed. Solutions: "
            "solutions/src/retail_pipeline/transform.py, solutions/tests/test_regressions.py (9 tests, 6 fail on the original code), "
            "solutions/dbt_project/models/marts/fct_orders.sql.")
add_table(s, [["#", "Where", "Bug", "Impact"],
              ["B1", "parse_amount", "Thousands space kept, error swallowed", "366 orders, about 572k EUR ignored"],
              ["B2", "clean_orders", "Sort ascending + keep first keeps the oldest", "1,000 stale statuses, returns missed"],
              ["B3", "clean_orders", "Divides by FX rate instead of multiplying", "4,058 USD/CHF orders, 100 USD = 108.70"],
              ["B4", "fct_orders", "Join on payments fans out rows", "2,796 duplicates, about 901k EUR inflated"]],
          left=0.56, top=2.3, width=12.2, col_align=["l", "l", "l", "l"], font_size=13, header_size=13)

# 11 Chart
s = content(B, "Debrief: the bugs touch thousands of rows",
            "Business context finds business bugs: the pitfalls in CLAUDE.md match these bugs exactly",
            "Rows affected on the training dataset. Message: business context is what lets the agent find business bugs. "
            "The pitfalls in the model-answer CLAUDE.md match the bugs exactly.")
add_chart(s, "hbar", ["B1 amounts lost", "B2 stale status", "B3 wrong FX", "B4 duplicates"],
          [("Rows affected", [366, 1000, 4058, 2796])], family="blue")

# 12 Two kinds of tests
s = content(B, "Two kinds of tests, two moments", "Code is tested on every change, data on every load",
            "5.2, 15 min talk. Unit tests check that the code does what is expected on constructed cases; data tests check that the data "
            "respects the rules on every run.")
add_versus(s, ("Unit tests (pytest)", ["Verify the code on constructed cases", "e.g. parse_amount('1 234,50') == 1234.5",
                                       "Run on every change (CI)"]),
           ("Data tests (dbt, Python)", ["Verify the data on every run", "unique, not_null, accepted_values, relationships",
                                         "Run on every load (dbt build)"]),
           labels=("Code", "Data"))

# 13 Source anomalies
s = content(B, "Flag source anomalies, never fix them silently", "Also seen: upper-case emails. Report them, let the business decide",
            "Checks that detect anomalies in the source: to be flagged, not silently corrected. 209 negative amounts, 87 orders dated 2031, "
            "212 empty amounts, 2% duplicate customers, upper-case emails.")
add_kpis(s, [("209", "negative amounts"), ("87", "orders dated 2031"), ("212", "empty amounts"),
             ("2%", "duplicate customers")], family="blue")

# 14 Checklist
s = content(B, "Validating generated code: a 5-point checklist", "Five checks before you accept a change",
            "1 Existing tests pass AND a new test covers the change. 2 The diff touches only what was requested. 3 Key figures reconciled with "
            "an independent source (row counts, checksums). 4 No silent behaviour added (swallowed exception, masking default). "
            "5 Human review, ideally supported by an independent review (data-reviewer subagent, see HD4).")
add_flow(s, [("Tests", "Old pass, new one covers the change"), ("Scope", "Diff touches only what was asked"),
             ("Reconcile", "Row counts and checksums vs a source"), ("No silence", "No swallowed error or masking default"),
             ("Review", "Human plus independent subagent")],
         icons=["check-circle", "target", "chart-bar", "lock", "user-check"], family="blue")

# 15 Exercise 3.2
s = content(B, "Complete the quality checks in Python and dbt",
            "Exercise 3.2 (25 min): source anomalies are flagged, not deleted. Where and how do you flag them?",
            "Exercise 3.2, 25 min. Complete quality.py (4 TODO functions) and add missing dbt tests, including a singular test reconciling "
            "payments with orders. Solutions: solutions/src/retail_pipeline/quality.py and "
            "solutions/dbt_project/tests/assert_payments_reconcile_with_orders.sql. In step 1, run /data-quality-audit and compare with what is known.")
add_flow(s, [("Audit", "Run /data-quality-audit on orders.csv and compare"),
             ("Python", "Complete the 4 TODO functions in quality.py, with tests"),
             ("dbt", "Add relationships and a singular reconciliation test")],
         icons=["file-text", "settings", "database"], family="blue")

# 16 Break
section("Title_Slide_3", "Break", "15 minutes", "Take the break, then restart with Theme 6.")

# 17 Section 6
section("Title_Slide_2", "Theme 6: Integrations and automation", "Second part of the half-day",
        "6.1 toolbox (25 min), 6.2 MCP (25 min), 6.3 skills, hooks, automation (40 min), wrap-up (20 min).")

# 18 Toolbox
s = content(Y, "The Claude Code toolbox: seven building blocks", "Each block answers a different need",
            "CLAUDE.md/rules: permanent instructions (RetailCo: business pitfalls, conventions). Skill: reusable procedure "
            "(.claude/skills/<name>/SKILL.md), invoked with /name or loaded when its description matches (/dbt-model, /data-quality-audit). "
            "Subagent: specialised assistant with own context, tools, model (.claude/agents/<name>.md), e.g. data-reviewer (read-only). "
            "Hook: shell command run deterministically at a point in the cycle (ruff format, block secrets). MCP: standard protocol to plug "
            "external tools (dbt MCP, Snowflake MCP). Plugin: package bundling skills, agents, hooks, MCP for sharing (future Keyrus Data plugin). "
            "Headless mode: claude -p (nightly quality report). Old custom commands (.claude/commands/*.md) still work and are merged with skills.")
add_hub(s, "Claude Code",
        [("CLAUDE.md", "Permanent instructions"), ("Skill", "Reusable procedure"), ("Subagent", "Own context"),
         ("Hook", "Deterministic shell"), ("MCP", "External tools"), ("Plugin", "Package to share"),
         ("Headless", "claude -p")],
        icons=["file-text", "lightbulb", "users", "lock", "network", "layers", "rocket"], family="yellow")

# 19 Which block
s = content(Y, "Which block for which need?", "Rule of thumb",
            "Rule of thumb. For an external system, MCP or simply its CLI (gh, snow, dbt), often more context-efficient.")
add_table(s, [["You need...", "Use"],
              ["An instruction to follow most of the time", "CLAUDE.md"],
              ["An occasional multi-step procedure", "Skill"],
              ["A rule that applies 100% of the time", "Hook or deny permission"],
              ["Verbose work, or fresh eyes", "Subagent"],
              ["An external system", "MCP, or simply its CLI (gh, snow, dbt)"]],
          left=0.56, top=2.3, width=12.2, col_align=["l", "l"], font_size=14, header_size=14)

# 20 MCP demo
s = content(Y, "Demo: plug in the dbt MCP server", "dbt-mcp runs locally: model discovery, lineage, dbt commands",
            "DEMO SCRIPT (6.2). The official dbt Labs MCP server (dbt-mcp) runs locally with uvx and exposes model discovery, lineage and dbt "
            "command execution. 1 Run the claude mcp add command, then claude mcp list. 2 In Claude Code run /mcp to see the server status. "
            "3 Ask: 'with the dbt MCP server, list the models that depend on stg_orders and their tests'.")
with custom(s):
    box(s, 0.6, 2.1, 1.7, 0.6, "1 Add", family="yellow")
    code(s, 0.6, 2.8, 5.9, 2.3,
         "claude mcp add dbt \\\n  -e DBT_PROJECT_DIR=\"$PWD/dbt_project\" \\\n  -e DBT_PATH=\"$(which dbt)\" \\\n"
         "  -e DBT_PROFILES_DIR=\"$PWD/dbt_project\" \\\n  -- uvx dbt-mcp\nclaude mcp list", 11)
    box(s, 7.1, 2.1, 1.7, 0.6, "2 Check", family="yellow")
    code(s, 7.1, 2.8, 5.6, 0.9, "/mcp   # server status", 12)
    box(s, 7.1, 3.9, 1.7, 0.6, "3 Ask", family="yellow")
    code(s, 7.1, 4.6, 5.6, 1.3, "> with the dbt MCP server, list the models\n  that depend on stg_orders and their tests", 11)
    arrow(s, 6.5, 3.9, 7.1, 3.2)

# 21 Scopes
s = content(Y, "Three installation scopes for an MCP server", "Use ${VARIABLES} in .mcp.json: no secret in the file",
            "local (default, only you, this project); project (committed .mcp.json shared with the team, each member approves the server on "
            "first use); user (all your projects). Template: .mcp.json.example; ${VARIABLES} are read from the environment so no secret sits in the file.")
add_layers(s, [("user", ["All your projects"]),
               ("project", ["Committed .mcp.json", "Shared, approved on first use"]),
               ("local", ["Default", "Only you, this project"])], family="yellow")

# 22 MCP caution
s = kdeck.add(prs, "3_Text_Boxes", title="MCP acts with your rights: stay careful")
kdeck.fill(s, {24: "Least privilege", 1: "Test database, read-only role, never production credentials",
               25: "Mind the context", 21: "Avoid thousands of rows. Claude Code warns above 10,000 tokens of MCP output",
               26: "Trusted sources", 23: "Official vendor, Anthropic directory, internal review"})
icons(s, ["lock", "gauge", "shield-check"])
notes(s, "Snowflake offers a managed MCP server (an MCP SERVER object created in the account) exposing Cortex Analyst, Cortex Search, Cortex agents "
         "and SQL execution, with Snowflake RBAC. Configure it with a read-only role. Often-sufficient alternative: Claude uses the Snowflake CLI "
         "(snow sql -q ...) with a restricted role and an ask rule. Cautions: MCP acts with your rights, never production credentials. Responses enter "
         "the context; Claude Code warns above 10,000 tokens of MCP output. Only install servers from known sources (official vendor, Anthropic "
         "directory, internal review).")

# 23 Exercise 3.3
s = content(Y, "Plug in dbt-mcp and map tests to columns", "Exercise 3.3 (15 min). Prerequisite: uv installed",
            "Exercise 3.3, 15 min. Prerequisite: uv installed. 1 /mcp: is the server connected, which tools? 2 With MCP, produce the matrix "
            "model, tests, untested columns. 3 Compare with the same request without MCP (/mcp to disable): result, number of actions, consumption (/usage).")
add_flow(s, [("Connect", "claude mcp add dbt, then /mcp. Which tools appear?"),
             ("Produce", "Matrix: model, tests, untested columns"),
             ("Compare", "Same request without MCP: result, actions, /usage")],
         icons=["network", "chart-bar", "gauge"], family="yellow")

# 24 Anatomy of a skill
s = content(Y, "Anatomy of a skill", "Demo (10 min): open .claude/skills/dbt-model/SKILL.md",
            "SKILLS DEMO (10 min). Open .claude/skills/dbt-model/SKILL.md. Show: the description (it triggers automatic loading); $ARGUMENTS; "
            "allowed-tools (tools pre-approved while the skill runs). sql-review: disable-model-invocation: true (only via /sql-review) and the "
            "injection of a !`git diff ...` command executed before Claude reads the skill. data-quality-audit: context: fork + agent: Explore runs in "
            "a read-only subagent, only the report comes back. Then run /data-quality-audit data/raw/orders.csv and compare with the anomalies found by hand in 3.2.")
add_tree(s, "SKILL.md",
         [("description", ["Triggers automatic loading"]),
          ("Inputs", ["$ARGUMENTS", "allowed-tools"]),
          ("sql-review", ["disable-model-invocation", "Only via /sql-review"]),
          ("data-quality-audit", ["context: fork", "Read-only subagent"])], family="yellow")

# 25 Demo skill run
s = content(Y, "Demo: run the audit skill and compare", "Compare with the anomalies you found by hand in 3.2",
            "Run /data-quality-audit data/raw/orders.csv. Compare with the anomalies found by hand in Exercise 3.2.")
with custom(s):
    code(s, 0.6, 2.1, 12.1, 0.7, "/data-quality-audit data/raw/orders.csv", 14)
add_flow(s, [("Skill loads", "Description matched or /name typed"), ("Forked subagent", "Read-only Explore agent does the work"),
             ("Report returns", "Only the report enters your context")],
         icons=["lightbulb", "users", "file-text"], family="yellow", zone=(0.56, 3.1, 12.2, 3.7))

# 26 Hooks
s = content(Y, "Demo: three hooks guard the project", "Try it: ask to drop the raw.orders table in DuckDB. It is blocked, /hooks lists active hooks",
            "HOOKS DEMO (10 min). Open .claude/settings.json and the scripts in .claude/hooks/. protect-files.sh: PreToolUse on Edit|Write, blocks "
            "writes to .env, data/raw/, .git/, profiles.yml. block-destructive-sql.sh: PreToolUse on Bash, blocks rm -rf, DROP/TRUNCATE TABLE, DELETE "
            "without WHERE, dbt on prod. format-python.sh: PostToolUse on Edit|Write, ruff format + ruff check --fix, sends remaining errors back to "
            "Claude. Demo: ask 'drop the raw.orders table in DuckDB' -> blocked; Claude explains the block. /hooks lists active hooks.")
add_table(s, [["Hook", "Event", "Effect"],
              ["protect-files.sh", "PreToolUse on Edit|Write", "Blocks writes to .env, data/raw/, .git/, profiles.yml"],
              ["block-destructive-sql.sh", "PreToolUse on Bash", "Blocks rm -rf, DROP/TRUNCATE, DELETE without WHERE, dbt on prod"],
              ["format-python.sh", "PostToolUse on Edit|Write", "ruff format and check --fix, errors go back to Claude"]],
          left=0.56, top=2.4, width=12.2, col_align=["l", "l", "l"], font_size=13, header_size=13)

# 27 Hook mechanics
s = content(Y, "A hook is a guarantee, CLAUDE.md is a request", "Hook = guarantee. Instruction in CLAUDE.md = request",
            "Mechanics: the hook receives a JSON description of the action on standard input; exit code 2 = action blocked, and the error message "
            "is sent back to Claude, which adapts. Key message: a hook is a guarantee, an instruction in CLAUDE.md is a request.")
add_flow(s, [("Claude acts", "About to edit or run a command"), ("Hook runs", "Receives the action as JSON on stdin"),
             ("Exit code 2", "Action is blocked"), ("Claude adapts", "Gets the error message, tries another way")],
         icons=["rocket", "lock", "shield-check", "brain"], family="yellow")

# 28 Headless
s = content(Y, "Automate recurring tasks with claude -p", "Non-interactive mode for scripts, CI or a scheduled task",
            "Non-interactive mode, for scripts, CI or a scheduled task. dontAsk + a tool allowlist = nothing else can run. Consultant use cases: "
            "daily quality report, dbt documentation updates, CI failure triage, automatic PR review (HD4).")
with custom(s):
    code(s, 0.6, 2.1, 12.1, 1.5,
         "claude -p \"run /data-quality-audit data/raw/orders.csv and write the report to reports/quality.md\" \\\n"
         "  --permission-mode dontAsk \\\n  --allowedTools \"Read\" \"Edit(./reports/**)\" \"Bash(python *)\" \\\n"
         "  --output-format json > run.json", 11)
    xs = [0.6, 3.7, 6.8, 9.9]
    for x, (t, d) in zip(xs, [("Daily quality report", "Scheduled audit"), ("dbt docs", "Keep documentation updated"),
                              ("CI triage", "Explain failing builds"), ("PR review", "Automatic, covered in HD4")]):
        box(s, x, 4.5, 2.8, 1.2, t, d, family="yellow", style="soft")
        arrow(s, x + 1.4, 3.6, x + 1.4, 4.5)

# 29 Exercise 3.4
s = kdeck.add(prs, "3_Text_Boxes", title="Exercise 3.4 (15 min): build your own automation")
kdeck.fill(s, {24: "A. A skill", 1: "/explain-model <model>: grain, lineage, tests, untested columns. Try it on fct_orders",
               25: "B. A Stop hook", 21: "Run pytest -q after each response, send failures back. Beware infinite loops",
               26: "C. A script", 23: "nightly_quality.sh calls claude -p in dontAsk mode with an allowlist"})
icons(s, ["lightbulb", "lock", "rocket"])
notes(s, "Exercise 3.4, 15 min. Choose one. A: skill /explain-model <model> in .claude/skills/explain-model/SKILL.md documenting a dbt model "
         "(grain, upstream/downstream lineage, tests, untested columns) and proposing missing tests; test on fct_orders and stg_orders. "
         "B: Stop hook in .claude/settings.json running pytest -q at the end of each response and sending failures back (exit code 2); beware of "
         "infinite loops: the JSON received contains stop_hook_active. C: non-interactive script scripts/nightly_quality.sh calling claude -p in "
         "dontAsk mode with a tool allowlist to produce reports/quality.md.")

# 30 Recap
s = content(R, "Recap: three things to remember", "Reliable work and the right building block",
            "1 Test first, business edge cases, review the diff. 2 Data is tested on every load, code on every change. 3 CLAUDE.md = request; "
            "hook/permission = guarantee; skill = procedure; MCP = connection; subagent = separate context. Wrap-up is a 20 min discussion.")
add_cards(s, [("Test first", "Business edge cases, review the diff"),
              ("Two test moments", "Data on every load, code on every change"),
              ("Pick the right block", "CLAUDE.md asks, hook guarantees, skill = procedure, MCP = connection")],
          icons=["check-circle", "shield-check", "layers"], family="red")

# 31 Next
section("Title_Slide_4", "Next: Half-day 4", "Before then: push your fixes branch to the session repository, without merging",
        "For HD4: everyone pushes their fixes branch to the session repository (without merging). Questions and discussion.")

# 32 Closing
s = kdeck.add_closing(prs, title="Thank you", subtitle="Half-day 3 - Testing, Quality & Integrations")
notes(s, "Closing. Questions and discussion.")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "3-testing-quality-integrations.pptx")
kdeck.save(prs, out)
print("wrote", out)
