---
description: Low-cost Perplexity search for links and snippets
---

# Perplexity Search

Use this workflow when the user wants a cheap Perplexity lookup with links and snippets.

1. Ask for the search query if it was not provided with the workflow invocation.
2. Prefer the `perplexity_search` MCP tool from the `perplexity` server.
3. If the MCP tool is not exposed in the current runtime, run `python3 ~/.codeium/windsurf/skills/perplexity-search/search_only.py "<query>" --json` for a global Windsurf install, or `python3 perplexity_search_only/scripts/search_only.py "<query>" --json` when working from the repository root.
4. Return 3-5 best results with title, URL, date when available, and a short note.
5. Do not use `perplexity_ask`, `perplexity_reason`, or `perplexity_research`.
6. If the user asks for synthesis or a recommendation, explain that this requires `/perplexity-pro` or `/perplexity-research`.
