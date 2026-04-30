---
description: Fetch URL mode through Perplexity Sonar Pro fetch_url_content
---

# Perplexity Fetch URL

Use this workflow for Fetch URL mode when the user provides one or more URLs and wants content extracted or answered from those URLs.

1. Ask for the URL list if it was not provided with the workflow invocation.
2. Ask for a focused question only if the user wants Q&A rather than a summary.
3. Run `python3 ~/.codeium/windsurf/skills/perplexity-fetch-url/fetch_url_content.py <url> [url ...] --json` for a global Windsurf install, or `python3 perplexity-fetch-url-content/scripts/fetch_url_content.py <url> [url ...] --json` from the repository root.
4. Add `--mode qa --question "<question>"` for Q&A, or `--mode summary` for concise page summaries.
5. Add `--require-fetch` when the user needs confirmation that every requested URL was fetched.
6. Return the extracted answer, `fetched_urls`, `missing_requested_urls`, and `usage.cost.total_cost` when present.
7. Do not claim this returns raw HTML or a guaranteed complete verbatim page dump.
