# HD1 — Getting started with Claude Code

Prerequisite: the README has been followed through to `dbt build` (1 failing test expected). Work in `default` (Manual) mode.

---

## Exercise 1.1 — First contact with RetailCo (30 min)

1. Launch `claude` at the repository root. Check the model and the folder with `/status` (or the information shown at startup).
2. Ask these questions **without explaining anything else** and observe which files Claude opens:
   - "What does this project do? Give the architecture in 5 lines."
   - "What are the data sources and how many rows does each contain?"
   - "Run the unit tests and the `dbt build`, then summarise the results."
3. Ask: "read the .env file". What happens? Why? (hint: `.claude/settings.json`)
4. Cycle through the modes with `Shift+Tab`. Write down the name of each mode.
5. Type `/context`: what already fills the context window?

To note for the debrief: one thing that surprised you, one thing that worries you.

🚀 Going further: `claude -p "how many dbt models does this project contain?" --output-format json` — what could this mode be used for?

---

## Exercise 1.2 — Rewriting prompts (15 min)

Rewrite each prompt using the **Context → Goal → Constraints → Verification** framework, test both versions (with `/clear` between each) and compare the number of actions and the result.

| Weak prompt | Your version |
| --- | --- |
| "Add tests." | |
| "The pipeline is slow, optimise it." | |
| "Make a dbt model for sales by product." | |

Do not commit anything: `git checkout .` to undo after the exercise (or `Esc` ×2 → rewind).

---

## Exercise 1.3 — Write the project's `CLAUDE.md` (30 min)

1. Run `/init` and read the generated `CLAUDE.md`.
2. Question Claude about the **data** (not the code) to find what `/init` could not guess, for example:
   - "What amount formats are found in `data/raw/orders.csv`? Give counts, not rows."
   - "Can an `order_id` appear several times in `orders.csv`? Why?"
   - "What is the maximum number of payments per order?"
   - "What does `FX_TO_EUR` mean in `config.py`?"
3. Add to `CLAUDE.md` a **"Business pitfalls"** section and a **"Security"** section. Stay under 80 lines.
4. Test: `/clear`, then "how should I join payments to orders?". Does the answer use your `CLAUDE.md`?
5. Create a `CLAUDE.local.md` with a personal preference (e.g. "answer in French, be concise") and check that it is indeed ignored by Git.

---

## Exercise 1.4 — Plan Mode (15 min)

Feature: add to the pipeline a `--since YYYY-MM-DD` option that loads only orders placed on or after that date.

1. Switch to Plan Mode (`Shift+Tab`).
2. Ask for a plan: impacted files, tests to write, edge cases (invalid date, future date, format).
3. **Have your neighbour approve the plan** and amend it at least once.
4. Leave Plan Mode and have it implemented, tests included. Verify with `pytest -q`.
5. Review the diff (`git diff`). Was everything that changed foreseen in the plan?
