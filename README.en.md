# Perplexity MCP Skills

A set of Codex skills for Perplexity: low-cost search, deep research, Pro Search, and reading page content by URL.

[🇷🇺 Читать на русском](README.md)

The skills are intentionally separated. This makes it easier to control cost and request depth: a quick search should not accidentally become an expensive research task, and reading a specific URL should not be mixed with general search.

Official links:

- [Perplexity documentation](https://docs.perplexity.ai/docs/getting-started/overview)
- [Perplexity console for API keys](https://console.perplexity.ai/)

## What's included

| Skill | When to use | What it calls | What it returns |
| --- | --- | --- | --- |
| `$perplexity_search_only` | You need links, sources, and snippets | MCP `perplexity_search` | A list of found pages without a model-generated answer |
| `$perplexity-pro-search` | You need a short answer with sources, but not deep research | Sonar Pro API with `search_type=pro` | Answer, sources, usage, and step log |
| `$perplexity_deep_research` | You need a broad review based on many sources | MCP `perplexity_research` | A detailed report with links |
| `$perplexity-fetch-url-content` | You need to read known URLs | Sonar Pro API and built-in `fetch_url_content` | Extracted page content and a check of which URLs were read |

## Quick setup

### 1. Get a Perplexity key

Create an API key in the [Perplexity console](https://console.perplexity.ai/). Do not put the key into repository files.

### 2. Add the official Perplexity MCP server to Codex

```bash
codex mcp add perplexity --env PERPLEXITY_API_KEY="your_key" -- npx -y @perplexity-ai/mcp-server
```

This command is required for `$perplexity_search_only` and `$perplexity_deep_research`. The direct scripts for Pro Search and URL reading can also read the key from the same Codex settings file.

If you do not want to add the MCP server, you can set the key through an environment variable before running the direct scripts:

```bash
export PERPLEXITY_API_KEY="your_key"
```

### 3. Download the repository and install the skills

```bash
git clone https://github.com/nicshik/perplexity-mcp-skills.git
cd perplexity-mcp-skills
./scripts/install_to_codex.sh
```

The installer copies the skills to `${CODEX_HOME:-$HOME/.codex}/skills`.

### 4. Restart Codex

After restart, call the skills explicitly:

```text
$perplexity_search_only <query>
$perplexity-pro-search <query>
$perplexity_deep_research <query>
$perplexity-fetch-url-content <url> [url ...]
```

## How to choose a skill

### `$perplexity_search_only`

The lowest-cost mode. Use it when you need links and short search-result details, not a ready-made model answer.

Use it for:

- finding official documentation;
- collecting 3-5 sources on a topic;
- checking a fresh news item;
- finding a page, repository, article, or primary source.

Limits:

- uses only `perplexity_search`;
- should not switch to `perplexity_ask`, `perplexity_reason`, or `perplexity_research`;
- does not read full page text;
- does not do deep analysis.

Example:

```text
Use $perplexity_search_only to find the official Perplexity MCP server documentation and return the 5 best links with short notes.
```

### `$perplexity-pro-search`

A middle mode between link search and deep research. Use it when you need a ready answer with sources, but deep research would be too costly or slow.

What it does:

- runs `perplexity-pro-search/scripts/pro_search.py`;
- uses `sonar-pro`;
- enables `search_type=pro`;
- receives the answer as a stream;
- saves sources, usage, and the step log.

How it differs from the official MCP `perplexity_ask`:

- both are useful for quick answers with sources;
- `perplexity_ask` is simpler and goes through the official MCP server;
- this skill is useful when you need to explicitly enable Pro Search and see the step log;
- for a normal question with sources, `perplexity_ask` is often enough.

Use it for:

- comparing several recent launches or products;
- quickly reviewing documentation changes;
- getting an answer from current sources without a long research run;
- checking what steps Sonar Pro performed.

Example:

```bash
python3 perplexity-pro-search/scripts/pro_search.py "Compare current Perplexity MCP server setup options for Codex and Cursor." --context-size medium --json
```

### `$perplexity_deep_research`

The heaviest mode. Use it when you need a broad and careful review of a topic across many sources.

Use it for:

- market or ecosystem reviews;
- comparing many competitors;
- researching a topic where different viewpoints matter;
- preparing a detailed brief before making a decision.

Limits:

- more expensive and slower than the other modes;
- uses only `perplexity_research`;
- should not be used for simple link search;
- it is better to narrow the question before running it.

Example:

```text
Use $perplexity_deep_research to research the current ecosystem of MCP servers for web search. Give a practical and concise conclusion.
```

### `$perplexity-fetch-url-content`

A mode for reading specific URLs. Use it when the page is already known and you need to extract its content.

What it does:

- runs `perplexity-fetch-url-content/scripts/fetch_url_content.py`;
- asks Sonar Pro to use the built-in `fetch_url_content`;
- returns extracted text or an answer based on the page;
- shows `fetched_urls` and `missing_requested_urls`, so you can see which URLs were read.

Important limit:

Perplexity `fetch_url_content` is not a separate MCP tool or a separate HTTP method. It is a built-in Pro Search capability that the model uses on its own. Because of that, this skill is not a strict HTML parser and does not guarantee a verbatim dump of the entire page text.

Use it for:

- extracting page content;
- reading a report or PDF by link;
- finding API parameters in documentation;
- answering a question strictly from a given URL;
- checking whether Perplexity actually read the requested URLs.

Examples:

```bash
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py https://docs.perplexity.ai/docs/sonar/pro-search/tools --json
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py https://example.com/report.pdf --question "Extract the methodology and key findings." --mode qa --json
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py https://example.com/a https://example.com/b --mode summary --require-fetch
```

## Installation check

Check help for the direct scripts:

```bash
python3 perplexity-pro-search/scripts/pro_search.py --help
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py --help
```

Check a request without calling the API:

```bash
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py --dry-run --json https://docs.perplexity.ai/docs/sonar/pro-search/tools
```

Check Python syntax:

```bash
python3 -m py_compile perplexity-pro-search/scripts/pro_search.py perplexity-fetch-url-content/scripts/fetch_url_content.py
```

Run live Perplexity checks manually: they spend API credits.

## Repository structure

```text
perplexity_search_only/
perplexity_deep_research/
perplexity-pro-search/
perplexity-fetch-url-content/
scripts/install_to_codex.sh
skills_manifest.yaml
```

## Notes

- The repository does not store API keys.
- Search and deep research skills require the Perplexity MCP server.
- Pro Search and URL reading skills use direct Sonar API calls, but read the key from the same Codex setting or from `PERPLEXITY_API_KEY`.
- If you need the full and exact text of a page, use a separate page parser. `fetch_url_content` is better suited for extracting useful content through Perplexity.
