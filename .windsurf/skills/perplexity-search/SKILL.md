---
name: perplexity-search
description: Low-cost Perplexity search mode. Use when the user needs links, sources, snippets, or quick web lookup without answer synthesis or deep research.
---

# Perplexity Search

Use this skill for cheap Perplexity web search only.

Rules:

- Use only the `perplexity_search` MCP tool from the `perplexity` server.
- Do not use `perplexity_ask`, `perplexity_reason`, or `perplexity_research`.
- Return 3-5 best results unless the user asks for another count.
- Include titles, URLs, dates when available, and short notes.
- If the user needs synthesis or recommendations, say that this requires a heavier mode.
