# Assessment

## End-of-training quiz (10 questions, 10 min)

1. **What is the main difference between an agent like Claude Code and a chat assistant?**
   a) It uses a better model · b) **It acts in a loop: gather context, act with tools, verify** · c) It does not send data to the cloud · d) It never makes mistakes
2. **A rule must apply 100% of the time ("never modify `data/raw/`"). Where do you put it?**
   a) `CLAUDE.md` · b) A skill · c) **A `deny` permission or a `PreToolUse` hook** · d) The prompt
3. **In which mode does Claude explore and propose a plan without modifying any file?**
   a) `acceptEdits` · b) **`plan`** · c) `dontAsk` · d) `bypassPermissions`
4. **You move from a bug fix to an unrelated documentation task. The right move?**
   a) Carry on · b) **`/clear`** · c) Change model · d) Restart the computer
5. **A dbt model joins payments to orders and the `unique` test on `order_id` fails. Most likely cause?**
   a) A dbt bug · b) **A fan-out: several payments per order, to be aggregated before the join** · c) A `NULL` in `order_id` · d) A permissions problem
6. **Claude proposes to fix a failing test by changing the test's assertion. What do you do?**
   a) Accept if CI passes · b) **Refuse until I have established that the test was wrong; otherwise fix the code** · c) Delete the test · d) Add a `try/except`
7. **What should a project `CLAUDE.md` ideally contain?**
   a) A description of every file · b) **Build/test commands, conventions, business pitfalls, prohibitions** · c) Login credentials · d) Session history
8. **For client code, which type of account should you use?**
   a) My personal Pro account · b) **A commercial account (Team/Enterprise, API or cloud), with no training on data by default** · c) Any of them · d) A free account
9. **Which lever reduces consumption the most over a long session?**
   a) Writing in English · b) **Keeping the context small: `/clear`, a short `CLAUDE.md`, skills on demand, subagents for verbose output** · c) Disabling tests · d) Always using Opus
10. **In GitHub Actions, how do you make an automatic PR review safe and controlled?**
   a) `bypassPermissions` · b) **Tool allowlist (`--allowedTools`), `--max-turns`, timeout, secret in GitHub secrets, final human review** · c) API key in the workflow · d) Let Claude merge the PR

Answers: 1b · 2c · 3b · 4b · 5b · 6b · 7b · 8b · 9b · 10b (shuffle the order of the answers before handing out).

## Case study grading grid (out of 20)

| Criterion | Points | Expected |
| --- | --- | --- |
| Scoping | 3 | Written assumptions (reference date, statuses, 365-day window, grain), business-relevant questions |
| Plan | 2 | Plan Mode used, plan validated before implementation, tests planned |
| dbt model correctness | 4 | VIP threshold, cancelled orders excluded, future dates ignored, reproducible result (no `current_date`), no fan-out |
| Tests | 3 | `unique`/`not_null` key, business rule test, pytest tests for the export |
| Privacy | 3 | Email pseudonymised after normalisation, no personal data in clear in the export or in the conversation |
| Delivery | 3 | Clean commits, independent review, PR described (including use of Claude), CI green |
| Lessons learned | 2 | Cost recorded, concrete improvement to `CLAUDE.md` or a skill |
