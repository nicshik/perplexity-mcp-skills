---
name: perplexity-fetch-url
description: Read specific URLs through Perplexity Sonar Pro fetch_url_content. Use when the user provides one or more URLs and wants page content extracted or answered from those URLs.
---

# Perplexity Fetch URL

Use this skill when the user wants Perplexity to read known URLs.

Rules:

- Run `python3 perplexity-fetch-url-content/scripts/fetch_url_content.py <url> [url ...] --json` from the repository root.
- Use `--mode summary` for short summaries, `--mode qa --question "..."` for a focused question, and default max-text when the user asks to extract as much useful content as possible.
- Use `--require-fetch` when the user needs confirmation that every URL was actually fetched.
- Report `fetched_urls`, `missing_requested_urls`, and `usage.cost.total_cost` when present.
- Do not claim this returns raw HTML or a guaranteed complete verbatim page dump.
