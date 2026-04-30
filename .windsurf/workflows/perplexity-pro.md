---
description: Perplexity Pro Search with sources, reasoning steps, and usage cost
---

# Perplexity Pro Search

Use this workflow when the user wants a concise sourced answer through Sonar Pro Search.

1. Ask for the query if it was not provided with the workflow invocation.
2. Run `python3 ~/.codeium/windsurf/skills/perplexity-pro/pro_search.py "<query>" --context-size medium --json` for a global Windsurf install, or `python3 perplexity-pro-search/scripts/pro_search.py "<query>" --context-size medium --json` from the repository root.
3. Use `--context-size low` for small factual checks and `--context-size high` only when the user needs broader source coverage.
4. Do not replace this with `perplexity_search`, `perplexity_ask`, `perplexity_reason`, or `perplexity_research` unless the user asks.
5. Return the answer, key sources, and `usage.cost.total_cost` when present.
6. If the script reports an API-key error, check `PERPLEXITY_API_KEY`, Codex config, and Windsurf MCP config.
