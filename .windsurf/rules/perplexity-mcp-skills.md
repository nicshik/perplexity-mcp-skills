# Perplexity MCP Skills

Use these Perplexity modes explicitly. Do not route simple searches into expensive research unless the user asks for it.

## Modes

- `@perplexity-search` or `/perplexity-search`: prefer the Perplexity MCP `perplexity_search` tool. If it is not exposed in the current runtime, run `python3 ~/.codeium/windsurf/skills/perplexity-search/search_only.py "<query>" --json` for a global Windsurf install, or `python3 perplexity_search_only/scripts/search_only.py "<query>" --json` from the repository root. Return links, dates if available, and short notes.
- `@perplexity-research` or `/perplexity-research`: use only the Perplexity MCP `perplexity_research` tool. Use it for broad research where higher cost and longer runtime are acceptable.
- `@perplexity-pro` or `/perplexity-pro`: run `perplexity-pro-search/scripts/pro_search.py` for Sonar Pro Search with `search_type=pro`.
- `@perplexity-fetch-url` or `/perplexity-fetch-url`: run `perplexity-fetch-url-content/scripts/fetch_url_content.py` when the user wants to read specific URLs.
- `$perplexity_search_only`: prefer the Perplexity MCP `perplexity_search` tool. If it is not exposed in the current runtime, run `python3 ~/.codeium/windsurf/skills/perplexity-search/search_only.py "<query>" --json` for a global Windsurf install, or `python3 perplexity_search_only/scripts/search_only.py "<query>" --json` from the repository root. Return links, dates if available, and short notes.
- `$perplexity_deep_research`: use only the Perplexity MCP `perplexity_research` tool. Use it for broad research where higher cost and longer runtime are acceptable.
- `$perplexity-pro-search`: run `perplexity-pro-search/scripts/pro_search.py` for Sonar Pro Search with `search_type=pro`.
- `$perplexity-fetch-url-content`: run `perplexity-fetch-url-content/scripts/fetch_url_content.py` when the user wants to read specific URLs.

## Cost control

- Prefer `@perplexity-search`, `/perplexity-search`, or `$perplexity_search_only` for finding sources.
- Use `@perplexity-research`, `/perplexity-research`, or `$perplexity_deep_research` only when the user explicitly asks for a deep review.
- Use direct scripts with `--json` when usage, cost, fetched URLs, or source details must be inspected.
- If the API key is missing, check `PERPLEXITY_API_KEY`, Codex config, and Windsurf MCP config.
