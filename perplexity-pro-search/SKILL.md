---
name: perplexity-pro-search
description: Direct workflow for Perplexity Pro Search API using a bundled script that calls Sonar Pro with streaming and `web_search_options.search_type=pro`. Use when the user explicitly wants Pro Search behavior or billing, not raw Search API or the cheaper Perplexity MCP search path.
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
    - cap.research.comparative_analysis
  distribution_scope: internal
  invocation_strategy: explicit
  version: v0.2
  source_of_truth: Skills/sources/internal/factorix/perplexity_pro_search
---

# Perplexity Pro Search

Use this skill when the user explicitly wants Perplexity `Pro Search API`, or when the task needs Sonar Pro's multi-step web workflow rather than raw ranked links.

This skill is explicit-only because Pro Search is materially more expensive than `Search API` and standard Sonar Pro fast search.

## Preconditions

- `PERPLEXITY_API_KEY` is available either in the shell environment or in `CODEX_HOME/config.toml` / `~/.codex/config.toml` under `mcp_servers.perplexity.env`.
- Network access to `https://api.perplexity.ai` is allowed.
- If the sandbox blocks outbound network calls, rerun the script with escalated permissions rather than silently downgrading.

## Non-Negotiable Rules

- Use the bundled `scripts/pro_search.py`.
- Keep `stream=true` and `web_search_options.search_type="pro"`.
- Do not silently downgrade to `perplexity_search`, `perplexity_ask`, `perplexity_reason`, or non-streaming Sonar Pro.
- Prefer `--json` when Codex needs to post-process the result.
- Keep scope sharp. Pro Search is for complex, comparative, or time-sensitive web questions, not trivial lookups.

## Lean Execution Rules

- Default to exactly one Pro Search API call.
- Do not inspect `scripts/pro_search.py` during routine use. Read it only if the skill is failing, being patched, or the user explicitly asks how it works.
- Do not add extra web, GitHub, or API verification after a successful Pro Search unless one of these is true:
  - the user explicitly asks for independent verification
  - the returned sources are not primary or official enough for the question
  - the answer appears internally inconsistent or conflicts with an official source
- If sandbox networking fails, rerun the same command once with escalation. Do not branch into alternative search tools.
- Keep commentary minimal. One short note before running and one short note if escalation is required is enough.

## Default Flow

1. Rewrite the user's request into a precise web question.
2. Choose filters only when they materially improve result quality:
   - `--context-size medium|high` for broader synthesis
   - `--recency` for current events
   - `--domain` to constrain sources
3. Run `scripts/pro_search.py` once, usually with `--json`.
4. Return a concise answer plus the strongest sources.
5. Include usage summary only when it is materially useful or the user asks.
6. If, and only if, the answer looks inconsistent or insufficiently official, do one targeted confirmation against the single strongest official source.
7. If the user only needs raw ranked links, recommend `$perplexity_search_only` instead.

## Recommended Commands

```bash
python3 scripts/pro_search.py "Compare the latest TON AI agent wallet launches and explain the differences." --context-size medium --json
python3 scripts/pro_search.py "Summarize this week's official TON docs changes." --recency week --domain docs.ton.org --json
python3 scripts/pro_search.py "Which open-source MCP servers added Perplexity support in 2026?" --context-size high --json
```

## Output Shape

- Default script output is human-readable: answer, sources, usage.
- `--json` returns structured data with `content`, `search_results`, `usage`, and optional reasoning traces so Codex can reformat it cleanly.
- If the API call fails, surface the error directly. Do not guess.

## References

- `references/prompt_recipes.md`
