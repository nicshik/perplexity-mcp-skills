---
name: perplexity_search_only
description: Internal workflow for low-cost Perplexity MCP web search only, without escalation into ask, reason, or deep research.
license: Factorix-Internal
compatibility:
  runtimes:
    - codex
    - claude_code
    - cursor
    - windsurf
metadata:
  category: research
  capability_taxonomy_ids:
    - cap.research.web_search
  distribution_scope: internal
  invocation_strategy: explicit
  version: v0.1
  source_of_truth: Skills/sources/internal/factorix/perplexity_search_only
---

# Perplexity Search Only

Use this skill when the user needs fresh web discovery through the Perplexity MCP server but does not want reasoning-heavy or research-heavy modes.

This skill is explicit-only because it should act as a deliberate low-cost path.

## Preconditions

- The `perplexity` MCP server is installed and enabled in Codex.
- `PERPLEXITY_API_KEY` is already configured in the MCP server environment.

## Non-Negotiable Rules

- Use `perplexity_search` only.
- Do not escalate to `perplexity_ask`, `perplexity_reason`, or `perplexity_research`.
- Return ranked links, dates when available, and concise takeaways.
- Keep results bounded, usually `3-5` strongest hits unless the user asks for more.

## Default Flow

1. Rewrite the user question into a sharp search query if needed.
2. Run `perplexity_search`.
3. Return the most relevant results with one-line takeaways.
4. If the user later wants broader synthesis or recommendation, tell them to switch to a deeper Perplexity workflow such as `$perplexity_deep_research`.

## Recommended Prompt Shape

- `Use $perplexity_search_only to run a Perplexity search for "<query>" and return the top 5 results with one-line takeaways.`

## References

- `references/prompt_recipes.md`
