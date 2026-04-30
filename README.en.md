# Perplexity MCP Skills

A set of Codex skills for Perplexity: low-cost search, deep research, Pro Search, and reading page content by URL.

[🇷🇺 Читать на русском](README.md)

The skills are intentionally separated. This makes it easier to control cost and request depth: a quick search should not accidentally become an expensive research task, and reading a specific URL should not be mixed with general search.

<details>
<summary>Why not use one shared Perplexity MCP access without separation</summary>

The official Perplexity MCP server supports several different tools:

- `perplexity_search` — link and snippet search;
- `perplexity_ask` — Sonar-based question answering;
- `perplexity_research` — deep research;
- `perplexity_reason` — reasoning for complex tasks.

If an agent gets one shared access to all tools, it can decide which tool to use for each request. This automatic choice is convenient, but it makes spending less predictable: a simple request may be handled by a heavier tool than you expected.

This repository separates the skills so the mode is explicit:

- need low-cost search — use `$perplexity_search_only`;
- need a detailed review — use `$perplexity_deep_research`;
- need a Pro Search answer — use `$perplexity-pro-search`;
- need to read a specific URL — use `$perplexity-fetch-url-content`.

This makes it easier to understand in advance what type of request will run and why it may cost more or less.

</details>

Official links:

- [Perplexity documentation](https://docs.perplexity.ai/docs/getting-started/overview)
- [Perplexity console for API keys](https://console.perplexity.ai/)

## What's included

| Skill | When to use | What it calls | What it returns |
| --- | --- | --- | --- |
| `$perplexity_search_only` | You need links, sources, and snippets | MCP `perplexity_search`, or a direct Search API script if MCP is unavailable | A list of found pages without a model-generated answer |
| `$perplexity-pro-search` | You need a short answer with sources, but not deep research | Sonar Pro API with `search_type=pro` | Answer, sources, usage, and step log |
| `$perplexity_deep_research` | You need a broad review based on many sources | MCP `perplexity_research` | A detailed report with links |
| `$perplexity-fetch-url-content` | You need to read known URLs | Sonar Pro API and built-in `fetch_url_content` | Extracted page content and a check of which URLs were read |

## Quick setup

### 1. Get a Perplexity key

Create an API key in the [Perplexity console](https://console.perplexity.ai/). Do not put the key into repository files.

Important API balance note:

- A Perplexity Pro subscription no longer includes monthly API credits.
- Sonar API uses a separate balance in the [Perplexity console](https://console.perplexity.ai/).
- If the balance is empty, requests may fail with authorization or billing errors even when the API key is configured correctly.
- You can add funds in the API settings. See: [API billing](https://www.perplexity.ai/help-center/en/articles/10354847-api-settings-billing).

Observed cost examples for individual modes:

- `/perplexity-research`: one deep research run for the query “best practices for organizing GitHub” cost **`$1.38`**:
  - input tokens: `97` -> `$0.00`
  - output tokens: `8,411` -> `$0.07`
  - citation tokens: `42,528` -> `$0.09`
  - reasoning tokens: `297,086` -> `$0.89`
  - search queries: `67` -> `$0.34`
- `/perplexity-pro`: one recent Pro Search run for the same query cost **`$0.01819`**:
  - request cost: `$0.01`
  - input tokens: `21` -> `$0.00006`
  - output tokens: `542` -> `$0.00813`
- `/perplexity-search`: a recent example for the same query used `4` Search API requests at `$0.005` each and cost **`$0.02`**.

### 2. Add the official Perplexity MCP server

#### Option A: Codex

```bash
codex mcp add perplexity --env PERPLEXITY_API_KEY="your_key" -- npx -y @perplexity-ai/mcp-server
```

#### Option B: Windsurf

```bash
PERPLEXITY_API_KEY="your_key" ./scripts/install_to_windsurf.sh
```

The script adds the Perplexity MCP server to `~/.codeium/windsurf/mcp_config.json`. Restart Windsurf after that.

You can also add the setting manually:

```json
{
  "mcpServers": {
    "perplexity": {
      "command": "npx",
      "args": ["-y", "@perplexity-ai/mcp-server"],
      "env": {
        "PERPLEXITY_API_KEY": "your_key"
      }
    }
  }
}
```

The MCP server is required for `$perplexity_deep_research` and remains the preferred path for `$perplexity_search_only`. If the MCP search tool is not exposed in a given agent session, `$perplexity_search_only` can use a direct Search API script instead. The direct scripts for search, Pro Search, and URL reading can read the key from the shell environment, Codex settings, or `~/.codeium/windsurf/mcp_config.json`.

If you do not want to add the MCP server, you can set the key through an environment variable before running the direct scripts:

```bash
export PERPLEXITY_API_KEY="your_key"
```

Before running the direct Python scripts, install the repository dependencies:

```bash
python3 -m pip install -r requirements.txt
```

This avoids local CA certificate store issues on some Python installations.

Important: an MCP server being enabled in the UI does not always guarantee that its tool is exposed inside a specific agent session. The repository includes a direct Search API fallback for cheap search specifically for that case.

### 3. Download the repository

```bash
git clone https://github.com/nicshik/perplexity-mcp-skills.git
cd perplexity-mcp-skills
```

### 4. Install the skills for Codex

```bash
./scripts/install_to_codex.sh
```

The installer copies the skills to `${CODEX_HOME:-$HOME/.codex}/skills`.

### 5. Use Windsurf Skills and Workflows

For Windsurf, the repository includes three integration layers:

- `.windsurf/skills/` — manual invocation through `@perplexity-search`, `@perplexity-research`, `@perplexity-pro`, `@perplexity-fetch-url`.
- `.windsurf/workflows/` — slash commands through Trigger Workflow: `/perplexity-search`, `/perplexity-research`, `/perplexity-pro`, `/perplexity-fetch-url`.
- `.windsurf/rules/perplexity-mcp-skills.md` — shared routing and cost-control guidance.

If you work from this repository in Windsurf, the workspace skills and workflows are already in the workspace. If you want to use them globally in all projects, run:

```bash
PERPLEXITY_API_KEY="your_key" ./scripts/install_to_windsurf.sh
```

The installer copies:

- skills to `~/.codeium/windsurf/skills/`;
- workflows to `~/.codeium/windsurf/global_workflows/`;
- MCP config to `~/.codeium/windsurf/mcp_config.json`.

### 6. Restart Codex or Windsurf

After restarting Codex, call the skills explicitly:

```text
$perplexity_search_only <query>
$perplexity-pro-search <query>
$perplexity_deep_research <query>
$perplexity-fetch-url-content <url> [url ...]
```

In Windsurf, use short manual invocations:

```text
@perplexity-search <query>
@perplexity-pro <query>
@perplexity-research <query>
@perplexity-fetch-url <url> [url ...]
```

Or Trigger Workflow:

```text
/perplexity-search
/perplexity-pro
/perplexity-research
/perplexity-fetch-url
```

## How to choose a skill

### Quick start in Windsurf

In Windsurf, you do not need to write long prompts with internal MCP method names. Use `@` for Skills or `/` for Workflows:

| Task | Windsurf Skill | Windsurf Workflow | Codex Skill |
| --- | --- | --- | --- |
| Cheap link search | `@perplexity-search` | `/perplexity-search` | `$perplexity_search_only` |
| Get a Pro Search answer | `@perplexity-pro` | `/perplexity-pro` | `$perplexity-pro-search` |
| Deeply research a topic | `@perplexity-research` | `/perplexity-research` | `$perplexity_deep_research` |
| Read specific URLs | `@perplexity-fetch-url` | `/perplexity-fetch-url` | `$perplexity-fetch-url-content` |

### `$perplexity_search_only`

The lowest-cost mode. Use it when you need links and short search-result details, not a ready-made model answer.

It prefers MCP `perplexity_search`, but if that MCP tool is not exposed in the current runtime it can use `perplexity_search_only/scripts/search_only.py` as a direct fallback with the same cheap-search contract.

Use it for:

- finding official documentation;
- collecting 3-5 sources on a topic;
- checking a fresh news item;
- finding a page, repository, article, or primary source.

Limits:

- uses MCP `perplexity_search` or a direct Search API fallback without answer synthesis;
- should not switch to `perplexity_ask`, `perplexity_reason`, or `perplexity_research`;
- does not read full page text;
- does not do deep analysis.

Example:

```text
Use $perplexity_search_only to find the official Perplexity MCP server documentation and return the 5 best links with short notes.
```

You can also run the direct fallback manually:

```bash
python3 ~/.codeium/windsurf/skills/perplexity-search/search_only.py "Perplexity MCP server documentation" --json
python3 perplexity_search_only/scripts/search_only.py "Perplexity MCP server documentation" --json
```

### `$perplexity-pro-search`

A middle mode between link search and deep research. Use it when you need a ready answer with sources, but deep research would be too costly or slow.

Recent single-run cost example: the query “best practices for organizing GitHub” through Pro Search cost **`$0.01819`** (`$0.01` request cost, `21` input tokens, `542` output tokens).

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
python3 ~/.codeium/windsurf/skills/perplexity-pro/pro_search.py "Compare current Perplexity MCP server setup options for Codex and Cursor." --context-size medium --json
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
python3 ~/.codeium/windsurf/skills/perplexity-fetch-url/fetch_url_content.py https://docs.perplexity.ai/docs/sonar/pro-search/tools --json
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py https://docs.perplexity.ai/docs/sonar/pro-search/tools --json
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py https://example.com/report.pdf --question "Extract the methodology and key findings." --mode qa --json
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py https://example.com/a https://example.com/b --mode summary --require-fetch
```

## Installation check

Check help for the direct scripts:

```bash
python3 ~/.codeium/windsurf/skills/perplexity-pro/pro_search.py --help
python3 ~/.codeium/windsurf/skills/perplexity-fetch-url/fetch_url_content.py --help
python3 perplexity-pro-search/scripts/pro_search.py --help
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py --help
```

If you run the direct Python scripts outside MCP, install dependencies first:

```bash
python3 -m pip install -r requirements.txt
```

Check a request without calling the API:

```bash
python3 ~/.codeium/windsurf/skills/perplexity-fetch-url/fetch_url_content.py --dry-run --json https://docs.perplexity.ai/docs/sonar/pro-search/tools
python3 perplexity-fetch-url-content/scripts/fetch_url_content.py --dry-run --json https://docs.perplexity.ai/docs/sonar/pro-search/tools
```

Check Python syntax:

```bash
python3 -m py_compile ~/.codeium/windsurf/skills/perplexity-pro/pro_search.py ~/.codeium/windsurf/skills/perplexity-fetch-url/fetch_url_content.py
python3 -m py_compile perplexity-pro-search/scripts/pro_search.py perplexity-fetch-url-content/scripts/fetch_url_content.py
```

Run live Perplexity checks manually: they spend API credits.

## Repository structure

```text
perplexity_search_only/
perplexity_deep_research/
perplexity-pro-search/
perplexity-fetch-url-content/
perplexity_common.py
scripts/install_to_codex.sh
skills_manifest.yaml
```

## Notes

- The repository does not store API keys.
- Deep research requires the Perplexity MCP server.
- Cheap search prefers MCP but includes a direct Search API fallback.
- Pro Search and URL reading skills use direct Sonar API calls, and the global Windsurf install copies their local scripts and `requirements.txt` directly into the skill directories.
- If you need the full and exact text of a page, use a separate page parser. `fetch_url_content` is better suited for extracting useful content through Perplexity.
