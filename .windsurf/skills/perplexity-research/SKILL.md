---
name: perplexity-research
description: Deep Perplexity research mode. Use only for broad, important questions where higher cost and longer runtime are acceptable.
---

# Perplexity Research

Use this skill for deep research through Perplexity.

Observed billing example: the query “best practices for organizing GitHub” through `sonar-deep-research` cost `$1.38`, mainly from reasoning tokens and search queries.

Rules:

- Use only the `perplexity_research` MCP tool from the `perplexity` server.
- Do not silently replace it with `perplexity_search`, `perplexity_ask`, or `perplexity_reason`.
- Keep the question focused before running the tool.
- Return a practical summary with the strongest citations.
- Mention that this mode is slower and more expensive than simple search when relevant.
