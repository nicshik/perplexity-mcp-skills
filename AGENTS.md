# Perplexity MCP Skills

This repository packages four separate Perplexity modes for agentic coding tools such as Codex, Windsurf, Cursor, Claude Code, and AGENTS-compatible tools.

## Mode Routing

- Use **Search only** when the task needs links, snippets, dates, or source discovery without answer synthesis.
  - Preferred MCP path: `perplexity_search`
  - Direct fallback: `python3 perplexity_search_only/scripts/search_only.py "<query>" --json`
- Use **Pro Search** when the task needs a concise sourced answer with explicit `search_type=pro`.
  - Path: `python3 perplexity-pro-search/scripts/pro_search.py "<query>" --context-size medium --json`
- Use **Deep Research** only for broad multi-source research where higher cost and longer runtime are acceptable.
  - MCP-only path: `perplexity_research`
- Use **Fetch URL** when the task needs to read one or more specific URLs rather than perform general search.
  - Path: `python3 perplexity-fetch-url-content/scripts/fetch_url_content.py <url> [url ...] --json`

## Non-Negotiable Rules

- Do not silently switch between modes.
- Keep Search only separate from Pro Search and Deep Research.
- Do not replace Deep Research with a cheaper mode unless the user asks.
- Do not claim that Fetch URL returns guaranteed full raw HTML dumps.
- Prefer official or primary sources when the task depends on current facts.

## Verification

- Run `./scripts/check.sh` for an offline-safe repository smoke check.
- Use the direct scripts with `--dry-run` for config validation without spending API credits.
