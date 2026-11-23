# HD4 — Industrialize and deliver

---

## Exercise 4.1 — From branch to reviewed PR (20 min)

Starting from your Half-day 3 fixes branch:

1. Check that each fix is in a separate commit, in the `type(scope): message` format (if not: have Claude reorganize the history, **on your branch only**).
2. "Use the data-reviewer subagent to review my changes." Address the blocking remarks.
3. Also run `/security-review`: what does it check?
4. Have Claude draft the PR description (context, cause, fix, quantified impact, tests, use of Claude Code), then **proofread and correct it yourself**.
5. Create the PR with `gh pr create`. Wait for CI. If Claude's automatic review comments, reply to it with `@claude` in the PR.

---

## Exercise 4.2 — End-to-end case study (95 min, pairs)

> RetailCo's sales leadership wants to identify, every month, **customers at risk of churning** in order to trigger a retention campaign.
> A customer is "at risk" if they have placed no order for more than **90 days** (**60 days** for VIPs), while having placed
> **at least 2 orders** in the preceding 12 months.
> Deliverables: a dbt table the BI team can use, and a daily CSV export for the CRM tool **with no personal data in clear text**.

### Milestones

| # | Milestone | Deliverable | ✔ |
| --- | --- | --- | --- |
| 1 | **Scoping** (10 min) — ask your questions to the business (the trainer) | `docs/cas_pratique.md`: assumptions, definitions, reference date, grain | |
| 2 | **Exploration and plan** (15 min) — Plan Mode | Plan validated by the trainer: models reused, files created, tests | |
| 3 | **dbt model** (25 min) | `marts/mart_customers_at_risk.sql` + YAML (grain, tests); `dbt build` green | |
| 4 | **Python export** (20 min) | `src/retail_pipeline/export_at_risk.py` + tests; pseudonymized customer identifier | |
| 5 | **Delivery** (15 min) | Branch, `data-reviewer` review, PR described, CI green | |
| 6 | **Review** (5 min) | `/usage` readout; one line added to `CLAUDE.md` or a skill proposed | |

(`cas_pratique` in the file name means "case study"; the name is kept as-is in the sample project.)

### Requirements

- The result must be **reproducible**: same input, same reference date → same output.
- Cancelled orders and future dates must not skew the calculation.
- No name or email in clear text in the export; no customer data displayed in full in the conversation.
- Tests: at minimum `unique`/`not_null` on the key, a test of the business rule, and pytest tests for the export.

### Presentation (5 min per pair)

Your initial plan, what Claude did well, what you had to correct, the session cost, what you would change in the project's `CLAUDE.md` or skills.
