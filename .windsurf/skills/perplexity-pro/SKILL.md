---
name: perplexity-pro
description: Perplexity Pro Search mode through the local Sonar Pro script. Use when the user needs a concise sourced answer, Pro Search, reasoning/tool steps, or usage cost.
---

# Perplexity Pro Search

Use this skill for Sonar Pro Search through the repository script.

Rules:

- Run `python3 perplexity-pro-search/scripts/pro_search.py "<query>" --context-size medium --json` from the repository root.
- Use `--context-size low` for small factual checks and `--context-size high` only when needed.
- Do not replace this with `perplexity_search`, `perplexity_ask`, `perplexity_reason`, or `perplexity_research` unless the user asks.
- Report `usage.cost.total_cost` when present.
- Return the answer, key sources, and cost if available.
