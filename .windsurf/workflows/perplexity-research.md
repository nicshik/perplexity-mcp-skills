---
description: Deep Research mode for broad multi-source questions
---

# Perplexity Research

Use this workflow for Deep Research mode when the user explicitly wants deep research and accepts higher cost and longer runtime.

Observed billing snapshot after skill tests cost `$2.52`; most of it came from `sonar-deep-research`: 478,195 reasoning tokens (`$1.43`), 117 search queries (`$0.59`), 67,825 citation tokens (`$0.14`), and 15,158 output tokens (`$0.12`).

1. Ask for the research question if it was not provided with the workflow invocation.
2. Narrow the scope before running the tool: topic, timeframe, geography, competitors, documents, or decision criteria.
3. Use only the `perplexity_research` MCP tool from the `perplexity` server.
4. Do not silently replace it with `perplexity_search`, `perplexity_ask`, or `perplexity_reason`.
5. Return a concise practical synthesis with the strongest citations.
6. Mention that this mode is slower and more expensive than `/perplexity-search` when relevant.
