---
name: perplexity_deep_research
description: Internal workflow for Perplexity MCP deep research only, reserved for broad high-stakes multi-source analysis where higher spend is acceptable.
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
    - cap.research.deep_research
    - cap.research.comparative_analysis
  distribution_scope: internal
  invocation_strategy: explicit
  version: v0.1
  source_of_truth: Skills/sources/internal/factorix/perplexity_deep_research
---

# Perplexity Deep Research

Use this skill when the task explicitly needs exhaustive multi-source research through the Perplexity MCP server and higher cost is acceptable.

This skill is explicit-only because `perplexity_research` can consume meaningfully more credits than search or reasoning modes.

## Preconditions

- The `perplexity` MCP server is installed and enabled in Codex.
- `PERPLEXITY_API_KEY` is already configured in the MCP server environment.

## Non-Negotiable Rules

- Use `perplexity_research` only.
- Do not silently downgrade to `perplexity_search`, `perplexity_ask`, or `perplexity_reason`.
- Keep the scope sharp even in deep research mode.
- Prefer practical synthesis over hype.

## Default Flow

1. Confirm the research question is broad enough to justify deep research.
2. Narrow the scope to the exact landscape, market, workflow, or competitor set.
3. Run `perplexity_research`.
4. Return a concise synthesis with the strongest citations.
5. If the user only needed links, recommend switching to `$perplexity_search_only` next time.

## Recommended Prompt Shape

- `Use $perplexity_deep_research to run a Perplexity deep research pass on "<question>". Focus on practical patterns, not hype, and keep it concise.`

## References

- `references/prompt_recipes.md`
