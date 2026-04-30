---
description: Low-cost Perplexity search for links and snippets
---

# Perplexity Search

Use this workflow when the user wants a cheap Perplexity lookup with links and snippets.

1. Ask for the search query if it was not provided with the workflow invocation.
2. Use only the `perplexity_search` MCP tool from the `perplexity` server.
3. Return 3-5 best results with title, URL, date when available, and a short note.
4. Do not use `perplexity_ask`, `perplexity_reason`, or `perplexity_research`.
5. If the user asks for synthesis or a recommendation, explain that this requires `/perplexity-pro` or `/perplexity-research`.
