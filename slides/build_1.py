# -*- coding: utf-8 -*-
"""Half-day 1 deck - Fundamentals, Prompting & Context (Keyrus template).

STORYBOARD (# | section | message | layout | visual | family)
 1 cover   | Half-day 1: Getting started with Claude Code | AI_Cover_Dark
 2 agenda  | 4 hours, 2 themes | Agenda_8_Items
 3 intro   | Welcome: who is in the room | Title_Description_Blue_Light | cards (4)
 4 S1      | Theme 1 intercalaire | Title_Slide_1
 5 S1      | A chat answers, an agent works | Blue | versus
 6 S1      | Agent loop | Blue | cycle
 7 S1      | What changes when the model can act | Blue | table
 8 S1      | Tools and surfaces | Blue | hub
 9 S1      | Demo: Claude explores RetailCo | Red | custom (task)
10 S1      | Which model | Blue | pyramid
11 S1      | Installation in 3 steps | Blue | flow
12 S1      | Essential commands | Blue | table
13 S1      | Six permission modes | Blue | table
14 S1      | Demo allow/ask/deny | Red | custom
15 S1      | Which setting wins | Blue | flow
16 S1      | Exercise 1.1 | Red | custom (task)
17 break  | Title_Slide_4
18 S2     | Theme 2 intercalaire | Title_Slide_2
19 S2     | Prompt = ticket | Yellow | flow
20 S2     | Bad vs good prompt | Yellow | table
21 S2     | Four more levers | Yellow | hub
22 S2     | Exercise 1.2 | Red | custom (task)
23 S2     | Context window is a budget | Yellow | custom
24 S2     | Four habits for context | Yellow | cards
25 S2     | CLAUDE.md locations | Yellow | table
26 S2     | What goes in CLAUDE.md | Yellow | versus
27 S2     | Demo path-scoped rules | Red | custom
28 S2     | Exercise 1.3 | Red | custom (task)
29 S2     | Plan Mode | Yellow | flow
30 S2     | Exercise 1.4 | Red | custom (task)
31 recap  | three ideas | Blue | cards
32 closing| add_closing
Native diagram slides: 18 of 26 content slides (69%); cards 3, tables 5.
"""
import sys
SKILL = ("C:/Users/Stefan.Duprey/.claude/plugins/synced/a8188927-62a2-4df9-9577-7c442b66f830_"
         "279e38b6-7f96-4e6c-900a-8904d25cb69d/keyrus-slides~g2/skills/keyrus-slides")
sys.path.insert(0, SKILL + "/scripts")
import kdeck
from diagrams import (add_flow, add_cards, add_cycle, add_versus, add_pyramid, add_hub,
                      custom, box, arrow, label)
from insert_table import add_table

OUT = "c:/Users/Stefan.Duprey/Documents/GitHub/keyrus-claude-code-training/slides/1-fundamentals-prompting-context.pptx"
prs = kdeck.new_deck()
NAVY = "021E57"


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text
    return s


def slide(layout, title, sub, note):
    return notes(kdeck.add(prs, layout, title=title, subtitle=sub), note)


def task(fam, kind, tag, dur, title, steps, note):
    s = slide(f"Title_Description_{fam}_Light", title, dur, note)
    n = len(steps)
    with custom(s):
        box(s, 0.56, 2.0, 3.0, 4.5, kind, tag, family="red", size=18)
        step = 4.5 / n
        rh = min(0.85, step - 0.1)
        for i, t in enumerate(steps):
            y = 2.0 + i * step
            box(s, 3.95, y, 8.8, rh, family="blue", style="soft")
            box(s, 4.1, y + (rh - 0.5) / 2, 0.5, 0.5, str(i + 1), family="navy", shape="oval", size=12)
            label(s, 4.8, y, 7.85, rh, t, size=12)
    return s


def section(layout, title, sub, note):
    s = kdeck.add(prs, layout, title=title)
    kdeck.fill(s, {20: sub})
    return notes(s, note)


# 1 Cover
notes(kdeck.add(prs, "AI_Cover_Dark", title="Half-day 1: Getting started with Claude Code",
                subtitle="Fundamentals, prompting and context engineering. Keyrus Claude Code training for data consultants"),
      "Session start time is up to the organiser. Duration: 4 hours including a 15 minute break.")

# 2 Agenda
s = kdeck.add(prs, "Agenda_8_Items", title="Agenda: 4 hours, 2 themes")
kdeck.fill(s, {16: "0:00  Welcome and expectations", 17: "0:15  1.1 From chat assistant to agent",
               18: "0:50  1.2 Install, configure, permissions", 19: "1:20  Exercise 1.1, then break (1:50)",
               20: "2:05  2.1 Effective instructions, Ex. 1.2", 21: "2:35  2.2 Context + Ex. 1.3 (3:00)",
               22: "3:30  2.3 Plan Mode + Exercise 1.4", 23: "3:50  Wrap-up, preparing half-day 2"})
notes(s, "Offsets are measured from the session start. The start time itself is decided by the organiser. "
         "Full timetable (elapsed, minutes): 0:00 (15) Welcome and expectations, discussion. 0:15 (35) 1.1 From chat assistant to agent, talk + demo. "
         "0:50 (30) 1.2 Installation, configuration, permissions, demo + practice. 1:20 (30) Exercise 1.1 first contact with RetailCo. "
         "1:50 (15) Break. 2:05 (30) 2.1 Writing effective instructions + Exercise 1.2. 2:35 (25) 2.2 Context: window, CLAUDE.md, memory, talk + demo. "
         "3:00 (30) Exercise 1.3 write the project CLAUDE.md. 3:30 (20) 2.3 Plan Mode + Exercise 1.4. 3:50 (10) Wrap-up and preparing half-day 2.")

# 3 Welcome
s = slide("Title_Description_Blue_Light", "Welcome: who is in the room?",
          "Round table, one sentence each",
          "Round table, one sentence each: role, usual stack (SQL/dbt/Python/Spark), current AI usage (none / ChatGPT / Copilot / Cursor / Claude Code). "
          "Note the already-users on the board: they act as reference buddies. Set the ground rules: 50% practice, one running project, we break things on purpose, never real client data during the training.")
add_cards(s, [("Your role", "Consultant, data engineer, analyst, architect"),
              ("Your stack", "SQL, dbt, Python, Spark, cloud warehouse"),
              ("Your AI usage", "None, ChatGPT, Copilot, Cursor or Claude Code"),
              ("Ground rules", "50% practice, one running project, break things on purpose, no real client data")],
          icons=["users", "database", "brain", "shield-check"], family="blue")

# 4 Section 1
section("Title_Slide_1", "Theme 1: Introduction and fundamentals", "From chat assistant to agent, installation, permissions", "Section 1 opener: from chat assistant to agent, installation, permissions.")

# 5 Chat vs agent
s = slide("Title_Description_Blue_Light", "A chat answers. An agent works.",
          "An LLM in chat mode receives text and returns text",
          "An LLM (Large Language Model) in chat mode receives text and returns text. You copy the code, run it, paste the error back. "
          "An agent receives a goal, then loops until the goal is reached or it needs you.")
add_versus(s, ("Chat assistant", ["Receives text, returns text", "You copy the code and run it", "You paste the error back"]),
           ("Agent (Claude Code)", ["Receives a goal, then loops", "Gathers context, acts with tools, checks", "Stops when done, or needs you"]),
           labels=("Chat", "Agent"))

# 6 Agent loop
s = slide("Title_Description_Blue_Light", "The agent loop: gather, act, verify",
          "Loops until done, or until a question for the human",
          "You can interrupt with Esc and redirect at any time. The loop continues until 'done' or a question to the human.")
add_cycle(s, [("Gather context", "Read files, search the repo"), ("Act", "Edit files, run a command"),
              ("Verify", "Tests, output, errors")], center="Esc to redirect")

# 7 What changes
s = slide("Title_Description_Blue_Light", "What changes when the model can act",
          "The risk moves from a wrong answer to a wrong action",
          "Main risk shifts from a wrong answer to a wrong action (overwritten file, dangerous command). Your role becomes project manager and reviewer.")
add_table(s, [["", "Chat assistant", "Agent (Claude Code)"],
              ["Access to code", "What you paste", "The whole repository, on demand"],
              ["Execution", "None", "Shell commands, tests, dbt, git"],
              ["Verification", "By you", "By itself, if you give it the means"],
              ["Unit of work", "One answer", "One task (dozens of actions)"],
              ["Main risk", "Wrong answer", "Wrong action"],
              ["Your role", "Question writer", "Project manager + reviewer"]],
          left=0.56, top=2.1, width=12.2, font_size=13, header_size=13)

# 8 Tools
s = slide("Title_Description_Blue_Light", "Tools and where to run Claude Code",
          "Same engine and same configuration files everywhere",
          "Show the tools in the demo without going into detail. MCP and skills are covered in half-day 3. Same engine and same configuration files everywhere.")
add_hub(s, "Claude Code", [("Built-in tools", "Read, Grep, Glob, Edit, Write, Bash"),
                           ("Web and agents", "WebFetch, WebSearch, subagents"),
                           ("Extensions", "MCP servers and skills (half-day 3)"),
                           ("Where it runs", "Terminal (our focus), IDEs, desktop, web, CI")],
        icons=["settings", "network", "rocket", "cloud"])

# 9 Demo 1
task("Red", "DEMO", "10 min", "Default mode, prompt on screen", "Demo: Claude explores RetailCo", [
    "Prompt: \"what does this project do? Give me the architecture in 5 lines and the command to run everything\"",
    "Point out: Claude read the README, pyproject.toml and listed src/ on its own",
    "Prompt: \"run the unit tests and tell me whether they pass\"",
    "Claude asks permission to run pytest: introduces permissions"],
    "DEMO SCRIPT (10 min). In the RetailCo repository, default mode, project the prompt: 'what does this project do? give me the architecture in 5 lines and the command to run everything'. "
    "Comment live: Claude received nothing but the question; it decides on its own to read the README and pyproject.toml and to list src/. Point out the tool calls displayed. "
    "Then: 'run the unit tests and tell me whether they pass'. Claude asks permission to run pytest (or not, if the project's allow rule covers it): a good opportunity to introduce permissions.")

# 10 Models
s = slide("Title_Description_Blue_Light", "Which model runs behind the scenes?",
          "Switch with /model; the agent infers the business",
          "Frequent question. /model lets you choose. We come back to costs in half-day 4. Do not promise that the agent understands the business: "
          "it infers from what it reads, hence the importance of CLAUDE.md (after the break).")
add_pyramid(s, [("Opus", "Complex reasoning"), ("Sonnet", "Default: most coding tasks"),
                ("Haiku", "Simple and fast tasks")], zone=(0.56, 1.95, 12.2, 4.3))
with custom(s):
    label(s, 0.56, 6.3, 12.2, 0.4, "That is why CLAUDE.md matters: the agent infers the business from what it reads.",
          size=12, bold=True, color=NAVY)

# 11 Installation
s = slide("Title_Description_Blue_Light", "Installation in three steps",
          "Normally done beforehand; native install recommended",
          "Normally done beforehand. Native install recommended with automatic updates. On native Windows, Git for Windows is recommended (otherwise Claude Code uses PowerShell as its shell); WSL does not need it. "
          "Sign-in options: Claude account (Pro, Max, Team, Enterprise), Claude Console (API), or cloud provider (Amazon Bedrock, Google Cloud, Microsoft Foundry). "
          "Alternatives: brew install --cask claude-code, winget install Anthropic.ClaudeCode.")
add_flow(s, [("Install", "Native installer, auto-updates"), ("Check", "claude --version"),
             ("Sign in", "Claude account, Console API or cloud provider")],
         icons=["rocket", "check-circle", "lock"], zone=(0.56, 1.95, 12.2, 3.6))
with custom(s):
    label(s, 0.56, 5.75, 12.2, 0.4, "macOS, Linux, WSL: curl -fsSL https://claude.ai/install.sh | bash", size=11, color=NAVY, bold=True)
    label(s, 0.56, 6.2, 12.2, 0.4, "Windows: irm https://claude.ai/install.ps1 | iex", size=11, color=NAVY, bold=True)

# 12 Commands
s = slide("Title_Description_Blue_Light", "Essential commands",
          "On the cheat sheet; claude -p is the basis for automation",
          "These are on the cheat sheet. claude -p is the basis for automation (half-days 3 and 4).")
add_table(s, [["Command", "Effect"],
              ["claude / claude \"task\"", "Interactive session, optionally with a first prompt"],
              ["claude -p \"question\"", "Headless mode: answers then exits (automation)"],
              ["claude -c / claude -r", "Resume last conversation / pick a conversation"],
              ["/clear   /context   /usage", "Empty context / see the window / see consumption"],
              ["/model   /effort", "Choose the model and the thinking level"],
              ["Esc   Esc x2 or /rewind", "Interrupt Claude / go back to a checkpoint"],
              ["Shift+Tab   @file   !cmd", "Cycle modes / reference a file / run a shell command"]],
          left=0.56, top=2.1, width=12.2, font_size=12, header_size=13)

# 13 Permission modes
s = slide("Title_Description_Blue_Light", "Six permission modes",
          "default is the training mode",
          "default is the training mode. bypassPermissions only in an isolated container or VM. Stress: deny rules apply in every mode, including bypassPermissions. "
          "Writes to .git, .claude, .mcp.json are never auto-approved (except in bypassPermissions).")
add_table(s, [["Mode", "Runs without asking", "Use"],
              ["default", "Reads only", "Discovery, sensitive code (training mode)"],
              ["acceptEdits", "Reads + file edits", "Iterating on code you review as you go"],
              ["plan", "Reads, no modifications", "Analyse and plan before touching code"],
              ["auto", "Everything, safety classifier", "Long tasks, if available and allowed"],
              ["dontAsk", "Reads + pre-approved tools", "CI and locked-down scripts"],
              ["bypassPermissions", "Everything", "Only in an isolated container or VM"]],
          left=0.56, top=2.1, width=12.2, font_size=12, header_size=13)

# 14 Settings demo
s = slide("Title_Description_Red_Light", "Demo: allow, ask, deny in settings.json",
          "Open .claude/settings.json and read it with the room",
          "DEMO. Open .claude/settings.json and read it with the room. allow: pytest, ruff, local dbt, read-only git. ask: git commit, git push, dbt on the Snowflake target. "
          "deny: reading .env and credential profiles, modifying data/raw/, curl/wget. Priority of settings: managed (enforced by IT) > command line > .claude/settings.local.json (personal, not committed) > "
          ".claude/settings.json (team, committed) > ~/.claude/settings.json (user). Live demonstration: 'read the .env file' is refused. First building block of the security part (half-day 4).")
with custom(s):
    for i, (fam, h, b) in enumerate([("blue", "allow", "pytest, ruff, local dbt, read-only git"),
                                     ("yellow", "ask", "git commit, git push, dbt on Snowflake"),
                                     ("red", "deny", "Reading .env, editing data/raw/, curl, wget")]):
        x = 0.56 + i * 4.2
        box(s, x, 2.2, 3.8, 0.9, h, family=fam, size=18)
        box(s, x, 3.2, 3.8, 1.7, b, family=fam, style="soft", size=13)
    label(s, 0.56, 5.3, 12.2, 0.4, "No friction on safe actions - human confirmation on risky ones - blocked on sensitive ones",
          size=12, bold=True, color=NAVY)
    label(s, 0.56, 5.9, 12.2, 0.4, "Live: ask Claude to read the .env file. Refused.", size=12, bold=True, color="DB0024")

# 15 Priority
s = slide("Title_Description_Blue_Light", "Which setting wins?",
          "Strongest on the left, weakest on the right",
          "Priority order of settings, from strongest to weakest.")
add_flow(s, [("Managed", "Enforced by IT"), ("Command line", "Flags for this run"),
             ("settings.local", "Personal, not committed"), ("settings.json", "Team, committed"),
             ("~/.claude", "User defaults")],
         icons=["lock", "settings", "user-check", "users", "file-text"])

# 16 Exercise 1.1
task("Red", "EXERCISE", "Ex 1.1", "30 min, individual", "Exercise 1.1: first contact with RetailCo", [
    "Launch claude at the repo root, check model and folder with /status",
    "Ask what the project does and what the data sources are; run the tests and dbt build",
    "Ask Claude to read .env: what happens and why?",
    "Cycle the permission modes with Shift+Tab and note their names",
    "Type /context: what already fills the window?"],
    "Goal: everyone has a working session, has seen Claude read, execute and answer, and has met a permission request. Walk the room: unblock failed installations first. "
    "After 20 min, have 2 or 3 people share their answers to 'what surprised you?'. Exercise sheet: exercises/HD1_getting_started.md. "
    "Stretch goal: claude -p with --output-format json, what could this mode be used for?")

# 17 Break
section("Title_Slide_4", "Break", "15 minutes. Back at 2:05", "Break, 15 minutes. Back at 2:05 elapsed.")

# 18 Section 2
section("Title_Slide_2", "Theme 2: Prompting and context engineering", "Instructions, context window, CLAUDE.md, Plan Mode", "Section 2 opener: instructions, context window, CLAUDE.md, Plan Mode.")

# 19 Prompt = ticket
s = slide("Title_Description_Yellow_Light", "A good prompt is a good ticket",
          "Treat the prompt like a Jira ticket, not an incantation",
          "A good prompt for an agent is not an incantation, it is a good Jira ticket: context, goal, constraints, definition of done. "
          "Formula to remember: Context, Goal, Constraints, Verification.")
add_flow(s, [("Context", "Where, which files, what exists"), ("Goal", "What outcome you want"),
             ("Constraints", "What must not change"), ("Verification", "How we know it is done")],
         icons=["file-text", "target", "lock", "check-circle"], family="yellow")

# 20 Bad vs good
s = slide("Title_Description_Yellow_Light", "Bad prompt, good prompt",
          "Be specific, point to files, verify, give an example",
          "Walk through each row. Further principles: point to files with @, give a verification criterion, set constraints, give an example, one task at a time, let it explore first.")
add_table(s, [["Principle", "Bad", "Good"],
              ["Be specific", "fix the bug", "In transform.clean_orders, duplicates keep the old version: keep the latest updated_at"],
              ["Point to files", "look at the orders model", "look at @dbt_project/models/marts/fct_orders.sql"],
              ["Verify", "add tests", "add a failing test, fix, then run pytest -q until green"],
              ["Example", "format the amounts", "'1 234,50' becomes 1234.5, '' becomes None"]],
          left=0.56, top=2.2, width=12.2, font_size=12, header_size=13)

# 21 Four levers
s = slide("Title_Description_Yellow_Light", "Four more levers",
          "Also: paste the full error, let Claude interview you",
          "Constraints example: without adding a dependency, SQL compatible with Snowflake and DuckDB, do not change the public API. "
          "Let it explore first: read the relevant code and explain how X should fit in, do not modify anything. Also: paste the full error or a screenshot, and ask Claude to interview you when the need is vague.")
add_hub(s, "Better prompts", [("Constraints", "No new dependency, keep the API"),
                              ("One task at a time", "Verify between each request"),
                              ("Explore first", "Read, explain, change nothing"),
                              ("Correct early", "Esc as soon as direction is wrong")],
        icons=["lock", "target", "lightbulb", "gauge"], family="yellow")

# 22 Exercise 1.2
task("Red", "EXERCISE", "Ex 1.2", "15 min, built in", "Exercise 1.2: rewrite weak prompts", [
    "Take the 3 weak prompts: add tests / pipeline is slow, optimise / make a dbt model for sales by product",
    "Rewrite each with Context, Goal, Constraints, Verification",
    "Test both versions, with /clear between each",
    "Compare actions and result quality. Do not commit: git checkout . afterwards"],
    "Participants rewrite 3 weak prompts from the exercise sheet, test them, and compare the number of actions and the quality of the result. Debrief: have the best prompt in the room read aloud.")

# 23 Context window
s = slide("Title_Description_Yellow_Light", "The context window is your budget",
          "Everything Claude knows in a session must fit in it",
          "Everything Claude knows during a session fits in its context window: system instructions, CLAUDE.md, history, contents of files read, command outputs. "
          "Fuller means each exchange costs more because everything is sent again with every request, and old off-topic information dilutes attention.")
with custom(s):
    items = ["System instructions", "CLAUDE.md", "History", "Files read", "Command outputs"]
    fams = ["navy", "blue", "cyan", "yellow", "red"]
    box(s, 0.56, 2.1, 12.2, 1.6, family="blue", style="outline")
    for i, (t, f) in enumerate(zip(items, fams)):
        box(s, 0.76 + i * 2.38, 2.35, 2.2, 1.1, t, family=f, size=12)
    label(s, 0.56, 3.8, 12.2, 0.4, "Context window", size=12, bold=True, color=NAVY, align="center")
    arrow(s, 6.66, 4.25, 6.66, 4.75)
    for i, (h, b, f) in enumerate([("100%", "of the history is sent again with every request", "navy"),
                                   ("Cost", "grows as the window fills up", "yellow"),
                                   ("Focus", "drops when old, off-topic content piles up", "red")]):
        box(s, 0.56 + i * 4.2, 4.85, 3.8, 1.5, h, b, family=f, style="soft", size=16)

# 24 Habits
s = slide("Title_Description_Yellow_Light", "Four habits to manage context",
          "See it, reset it, summarise it, delegate it",
          "/rename before /clear to find the session again. /compact example: /compact keep the modified files and the test results. Subagents are covered in half-day 3.")
add_cards(s, [("/context", "See what fills the window"), ("/clear", "Between two unrelated tasks. It is free"),
              ("/compact", "Summarise a long session, keep the essentials"),
              ("Subagents", "Delegate verbose work: only the summary comes back")],
          icons=["gauge", "settings", "layers", "network"], family="yellow")

# 25 CLAUDE.md locations
s = slide("Title_Description_Yellow_Light", "CLAUDE.md: the project memory",
          "Every session starts blank; all files found are concatenated",
          "Every session starts blank. CLAUDE.md is a Markdown file loaded automatically at startup. All files found are concatenated, not replaced. A file can import another with @path/file. "
          "There is also an automatic memory that Claude writes from your corrections; /memory lets you view and edit everything.")
add_table(s, [["Location", "Scope", "Committed?"],
              ["Company policy (/etc/claude-code/CLAUDE.md)", "Whole organisation, enforced by IT", "n/a"],
              ["~/.claude/CLAUDE.md", "You, all your projects", "No"],
              ["./CLAUDE.md", "The project, the whole team", "Yes"],
              ["./CLAUDE.local.md", "You, this project (in .gitignore)", "No"],
              ["subfolder/CLAUDE.md", "Loaded when working in that subfolder", "Yes"],
              [".claude/rules/*.md with paths:", "Only for matching files", "Yes"]],
          left=0.56, top=2.1, width=12.2, font_size=12, header_size=13)

# 26 What goes in
s = slide("Title_Description_Yellow_Light", "What goes in CLAUDE.md, and what does not",
          "CLAUDE.md is context, not a constraint: aim for under 200 lines",
          "CLAUDE.md is context, not a constraint. Guaranteed rules belong in deny permissions or hooks. Aim for fewer than 200 lines: beyond that, adherence drops and cost rises.")
add_versus(s, ("Commands and conventions", ["Exact build and test commands", "Business pitfalls (French amount format, 2 payments per order)",
                                            "Team conventions (dbt naming, commit format)", "Prohibitions (never run dbt on prod)"]),
           ("What Claude can find itself", ["A description of every file: Claude can read", "Long, rare procedures: use skills (half-day 3)",
                                            "Guaranteed rules: use deny permissions or hooks"]),
           labels=("Put in", "Leave out"), zone=(0.56, 1.95, 12.2, 4.3))
with custom(s):
    label(s, 0.56, 6.35, 12.2, 0.4, "Target: fewer than 200 lines.", size=12, bold=True, color=NAVY)

# 27 Rules demo
s = slide("Title_Description_Red_Light", "Demo: path-scoped rules",
          "5 min: open .claude/rules/dbt.md",
          "DEMO (5 min). Show .claude/rules/dbt.md: thanks to paths:, these rules enter the context only when Claude touches a dbt file.")
with custom(s):
    box(s, 0.56, 2.5, 3.3, 1.5, ".claude/rules/dbt.md", "paths: front-matter", family="navy", size=13)
    box(s, 4.85, 2.5, 3.3, 1.5, "Claude touches a dbt file", family="yellow", style="soft", size=13)
    box(s, 9.15, 2.5, 3.6, 1.5, "Rules enter the context", family="blue", size=13)
    arrow(s, 3.86, 3.25, 4.85, 3.25)
    arrow(s, 8.15, 3.25, 9.15, 3.25)
    box(s, 0.56, 4.6, 12.2, 1.1, "0 tokens spent on dbt rules until Claude touches a dbt file", family="cyan", style="soft", size=14)

# 28 Exercise 1.3
task("Red", "EXERCISE", "Ex 1.3", "30 min, practice", "Exercise 1.3: write the project CLAUDE.md", [
    "Run /init and read the generated CLAUDE.md",
    "Question Claude about the data (not the code) to find the business pitfalls",
    "Add Business pitfalls and Security sections, under 80 lines",
    "Test: /clear then ask how to join payments to orders. Is your CLAUDE.md used?",
    "Create CLAUDE.local.md and check Git ignores it"],
    "Participants critique and enrich the /init output with the business pitfalls they discover. Reference solution: solutions/CLAUDE.md. Do NOT show it before the end: "
    "the point is to see that /init does not find the business pitfalls on its own. The pitfalls listed in the solution are exactly the bugs hunted in half-day 3: this is intentional, and we will come back to it.")

# 29 Plan mode
s = slide("Title_Description_Yellow_Light", "Plan Mode: think before you write",
          "One task = one verifiable result; save big plans in PLAN.md",
          "Plan Mode (Shift+Tab until 'plan', or claude --permission-mode plan): Claude explores and proposes a plan without modifying anything. You approve, amend or reject before any write. "
          "Add 'think deeply' for complex topics. Decompose: one task = one verifiable result. A 15-step plan is split into 3 sessions with /clear between them, the plan being saved in a file (PLAN.md).")
add_flow(s, [("Explore", "Read X and Y, change nothing"), ("Plan", "Plan Mode: steps, files, tests"),
             ("Implement", "Step by step"), ("Verify", "Tests, dbt build, diff"), ("Commit", "Once reviewed")],
         icons=["lightbulb", "target", "settings", "check-circle", "rocket"], family="yellow")

# 30 Exercise 1.4
task("Red", "EXERCISE", "Ex 1.4", "15 min, in pairs", "Exercise 1.4: add --since in Plan Mode", [
    "Switch to Plan Mode with Shift+Tab",
    "Ask for a plan for a --since YYYY-MM-DD option: files, tests, edge cases",
    "Have your buddy approve the plan, and amend it at least once",
    "Leave Plan Mode, implement, run pytest -q",
    "Review git diff: was everything foreseen in the plan?"],
    "Add to the pipeline a --since YYYY-MM-DD option that loads only orders after a given date. Plan Mode is mandatory and the plan must be approved by the buddy before implementation.")

# 31 Recap
s = slide("Title_Description_Blue_Light", "Recap: three ideas to keep",
          "Have the room state them first",
          "Have the room state the 3 ideas they retain first, then complete with these.")
add_cards(s, [("The agent acts", "So rely on permissions and review every diff"),
              ("Context is quality and cost", "Keep CLAUDE.md short and use /clear often"),
              ("Plan before coding", "Use Plan Mode for any non-trivial task")],
          icons=["shield-check", "gauge", "target"], family="blue")

# 32 Closing
notes(kdeck.add_closing(prs, title="See you in half-day 2",
                        subtitle="Keep your CLAUDE.md. Optional homework: read sql/legacy/customer_ltv.sql without Claude and note what looks suspicious."),
      "Wrap-up (10 min). For half-day 2: keep your CLAUDE.md; those who wish read the legacy query sql/legacy/customer_ltv.sql (without Claude!) and note what looks suspicious.")

kdeck.save(prs, OUT)
print("saved", OUT, len(prs.slides._sldIdLst))
