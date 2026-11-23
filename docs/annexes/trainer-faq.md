# Trainer FAQ and Common Incidents

## Frequently asked questions from participants

**"Does Claude keep my code to train on it?"**
Not with a commercial account (Team, Enterprise, API, cloud platforms): Anthropic does not train its models on this data unless the organisation opts in. Standard retention is 30 days, ZDR (Zero Data Retention) is possible on Enterprise. Consumer accounts (Free, Pro, Max) depend on the user's setting. See half-day 4, section 8.1.

**"Do we need one API key per participant?"**
No. Everyone signs in with their own account (Team/Enterprise seat, or member of a Claude Console organisation). Only the GitHub Actions demo uses a repository secret. See [00-preparation.md](../00-preparation.md).

**"What is the difference with GitHub Copilot or Cursor?"**
Stay factual and avoid disparagement: Claude Code is terminal- and agent-centred (autonomous loop, shell tools, hooks, subagents, MCP, non-interactive mode for CI). It can also be used in VS Code and JetBrains. The choice often depends on what the client allows.

**"Can we use it at a client that forbids sending code outside?"**
Not without the client's written agreement. Options to discuss with them: hosting in their own cloud (Amazon Bedrock, Google Cloud, Microsoft Foundry), ZDR, working on synthetic data. When in doubt: no.

**"Can Claude connect directly to our Snowflake?"**
Yes, through the `snow` CLI or an MCP server (including Snowflake's managed MCP server), **with a read-only role** and without identifying production data. See half-day 3, section 6.2.

**"How do we avoid approving 50 permission requests?"**
Pre-approve safe, frequent commands in `.claude/settings.json` (`allow`), use `acceptEdits` on code you review, the sandbox (`/sandbox`), or `auto` mode if the organisation allows it. Never `bypassPermissions` outside a container.

## Common incidents

| Symptom | Probable cause | Fix |
| --- | --- | --- |
| `claude: command not found` after installation | Install folder missing from the PATH | Open a new terminal; see the *Troubleshoot installation* page of the documentation |
| `The token '&&' is not a valid statement separator` | CMD command run in PowerShell | Use `irm https://claude.ai/install.ps1 \| iex` |
| Hooks do not fire | Script not executable or `jq` missing | `chmod +x .claude/hooks/*.sh`, install `jq`, check with `/hooks` |
| Hooks fail on native Windows | Bash scripts | Use WSL or Git for Windows |
| `dbt build`: "Could not find profile" | `DBT_PROFILES_DIR` not set | Run from `dbt_project/` with `DBT_PROFILES_DIR=.` |
| DuckDB: "Could not set lock on file" | Two processes open `retail.duckdb` (e.g. a notebook + dbt) | Close the other connection |
| dbt MCP server "failed" | `uvx` not found in Claude Code's PATH | Give the full path to `uvx` (`which uvx`) |
| Usage-limit message in the middle of a session | Seat quota or organisation rate limit | Switch to Sonnet, `/clear`, plan a higher rate limit for group sessions |
| Claude "goes in circles" | Polluted context, vague goal | `Esc`, `/clear`, rephrase with a verification criterion |
| A participant "broke everything" | — | `git stash` or `git checkout state-hdN` (fallback branches) |
