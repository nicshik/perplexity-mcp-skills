# Perplexity MCP Skills

Use these Perplexity modes explicitly. Do not route simple searches into expensive research unless the user asks for it.

## Modes

- `$perplexity_search_only`: use only the Perplexity MCP `perplexity_search` tool. Return links, dates if available, and short notes.
- `$perplexity_deep_research`: use only the Perplexity MCP `perplexity_research` tool. Use it for broad research where higher cost and longer runtime are acceptable.
- `$perplexity-pro-search`: run `perplexity-pro-search/scripts/pro_search.py` for Sonar Pro Search with `search_type=pro`.
- `$perplexity-fetch-url-content`: run `perplexity-fetch-url-content/scripts/fetch_url_content.py` when the user wants to read specific URLs.

## Cost control

- Prefer `$perplexity_search_only` for finding sources.
- Use `$perplexity_deep_research` only when the user explicitly asks for a deep review.
- Use direct scripts with `--json` when usage, cost, fetched URLs, or source details must be inspected.
- If the API key is missing, check `PERPLEXITY_API_KEY`, Codex config, and Windsurf MCP config.
