# Perplexity MCP Skills

A Perplexity mode bundle for Codex, Windsurf, Cursor, Claude Code, and Antigravity: low-cost search, Pro Search, deep research, and reading specific URLs.

[🇷🇺 Читать на русском](README.ru.md)

## What This Repo Is

This repository packages four separate Perplexity modes so cost, depth, and invocation style stay explicit across multiple agent runtimes:

- `Codex` uses explicit skill calls such as `$perplexity_*`.
- `Windsurf` uses skills `@perplexity-*` and workflows `/perplexity-*`.
- `Cursor` uses project MCP config plus project rules.
- `Claude Code` uses project MCP config plus project skills.
- `Antigravity` uses shared `AGENTS.md` guidance and the same repo-local scripts.

The separation is intentional: a quick lookup should not silently become expensive research, and reading a specific URL should not be mixed with general search.

## What To Pick In 30 Seconds

| Job | Mode | Codex | Windsurf | Needs MCP |
| --- | --- | --- | --- | --- |
| Find links and snippets | Search only | `$perplexity_search_only` | `@perplexity-search` / `/perplexity-search` | Preferred |
| Get a short answer with sources | Pro Search | `$perplexity-pro-search` | `@perplexity-pro` / `/perplexity-pro` | No |
| Run a broad multi-source review | Deep Research | `$perplexity_deep_research` | `@perplexity-research` / `/perplexity-research` | Yes |
| Read one or more known URLs | Fetch URL | `$perplexity-fetch-url-content` | `@perplexity-fetch-url` / `/perplexity-fetch-url` | No |

`Cursor`, `Claude Code`, and `Antigravity` use the same four modes through project configs and repository guidance instead of Codex/Windsurf-style invocation syntax. Their setup is documented below.

## Compatibility Matrix

| Mode | Codex | Windsurf | Needs MCP | Needs API key | Direct fallback | Typical cost/speed |
| --- | --- | --- | --- | --- | --- | --- |
| Search only | `$perplexity_search_only` | `@perplexity-search` / `/perplexity-search` | Preferred | Yes | Search API script | Cheapest, fast |
| Pro Search | `$perplexity-pro-search` | `@perplexity-pro` / `/perplexity-pro` | No | Yes | N/A | Medium cost, fast |
| Deep Research | `$perplexity_deep_research` | `@perplexity-research` / `/perplexity-research` | Yes | Yes | None | Highest cost, slowest |
| Fetch URL | `$perplexity-fetch-url-content` | `@perplexity-fetch-url` / `/perplexity-fetch-url` | No | Yes | N/A | Medium cost, page-dependent |

## Quick Setup

### 1. Get a Perplexity API key

Create an API key in the [Perplexity console](https://console.perplexity.ai/). Do not store the key in repository files.

Important billing note:

- A Perplexity Pro subscription no longer includes monthly API credits.
- Sonar API uses a separate balance in the [Perplexity console](https://console.perplexity.ai/).
- If the balance is empty, requests may fail with authorization or billing errors even when the key is configured correctly.

### 2. Add the official Perplexity MCP server

#### Codex

```bash
codex mcp add perplexity --env PERPLEXITY_API_KEY="your_key" -- npx -y @perplexity-ai/mcp-server
```

#### Windsurf

```bash
PERPLEXITY_API_KEY="your_key" ./scripts/install_to_windsurf.sh
```

The script adds the Perplexity MCP server to `~/.codeium/windsurf/mcp_config.json`.

You can also add MCP manually:

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

`$perplexity_deep_research` requires MCP. `$perplexity_search_only` still prefers the MCP path, but it has a direct Search API fallback if the tool is not exposed in the active runtime.

If you do not want MCP, the direct scripts can read the key from:

- `PERPLEXITY_API_KEY`
- `~/.codex/config.toml` or `CODEX_HOME/config.toml`
- `~/.codeium/windsurf/mcp_config.json`

Before running direct scripts, install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

### 3. Clone the repository

```bash
git clone https://github.com/nicshik/perplexity-mcp-skills.git
cd perplexity-mcp-skills
```

### 4. Enable invocation in your environment

#### Codex

```bash
./scripts/install_to_codex.sh
```

After that, the skills are available as explicit calls:

```text
$perplexity_search_only <query>
$perplexity-pro-search <query>
$perplexity_deep_research <query>
$perplexity-fetch-url-content <url> [url ...]
```

#### Windsurf

For Windsurf, the repository contains three integration layers:

- `.windsurf/skills/` for `@perplexity-search`, `@perplexity-research`, `@perplexity-pro`, `@perplexity-fetch-url`
- `.windsurf/workflows/` for `/perplexity-search`, `/perplexity-research`, `/perplexity-pro`, `/perplexity-fetch-url`
- `.windsurf/rules/perplexity-mcp-skills.md` for shared routing and cost control

To install them globally:

```bash
PERPLEXITY_API_KEY="your_key" ./scripts/install_to_windsurf.sh
```

The installer copies:

- skills to `~/.codeium/windsurf/skills/`
- workflows to `~/.codeium/windsurf/global_workflows/`
- MCP config to `~/.codeium/windsurf/mcp_config.json`

After restarting Windsurf, use:

```text
@perplexity-search <query>
@perplexity-pro <query>
@perplexity-research <query>
@perplexity-fetch-url <url> [url ...]
```

Or workflows:

```text
/perplexity-search
/perplexity-pro
/perplexity-research
/perplexity-fetch-url
```

#### Cursor

Cursor support is included through:

- project MCP config in `.cursor/mcp.json`
- project rule in `.cursor/rules/perplexity.mdc`
- the same repo-local direct scripts used elsewhere

After opening the repository in Cursor, the agent can use the configured MCP server and project rule. For CLI verification, Cursor documents `cursor-agent mcp list` and `cursor-agent mcp list-tools <identifier>` for inspecting configured servers and tools. Sources: Cursor MCP and Rules docs.

#### Claude Code

Claude Code support is included through:

- project MCP config in `.mcp.json`
- project skills in `.claude/skills/`

Claude Code documents project-scoped MCP config through `.mcp.json` and project skills through `.claude/skills/`. After opening the repository in Claude Code, the MCP server and project skills are available in-project. Sources: Claude Code MCP and Agent Skills docs.

#### Antigravity

Antigravity support is provided through the shared repository guidance in `AGENTS.md` plus the same repo-local direct scripts.

This rollout does not add a tool-specific Antigravity MCP config file because the repository does not encode an official stable project config path for Antigravity. The supported path here is shared routing guidance plus the local scripts and MCP setup you already use in the workspace.

## Examples By Job To Be Done

### Find sources quickly and cheaply

```text
Use $perplexity_search_only to find the official Perplexity MCP server documentation and return the 5 best links with short notes.
```

### Get a short answer with sources

```text
Use $perplexity-pro-search to compare the current Perplexity MCP setup options for Codex and Windsurf and return a concise sourced answer.
```

### Deeply research a topic

```text
Use $perplexity_deep_research to deeply research best practices for organizing GitHub. Focus on practical takeaways and keep the answer concise.
```

### Read a specific URL

```text
Use $perplexity-fetch-url-content to read https://docs.perplexity.ai/docs/sonar/pro-search/tools and summarize the key fetch_url_content limitations.
```

## Mode Guide

### Search only

The lowest-cost mode. Use it when you need links, dates, snippets, and primary sources without answer synthesis.

- Preferred path: MCP `perplexity_search`
- Direct fallback: `perplexity_search_only/scripts/search_only.py`
- It should not switch into `perplexity_ask`, `perplexity_reason`, or `perplexity_research`

### Pro Search

The middle mode between link lookup and deep research. Use it when you want a ready answer with sources and explicit `search_type=pro`.

- Path: `perplexity-pro-search/scripts/pro_search.py`
- Model path: `sonar-pro`
- Output: answer, sources, usage, step log

### Deep Research

The most expensive mode. Use it only for broad multi-source questions where longer runtime and higher cost are justified.

- Path: MCP `perplexity_research`
- Fallback: none
- Scope: keep the question narrow even in deep mode

### Fetch URL

The mode for reading specific URLs through the built-in Sonar Pro tool `fetch_url_content`.

- Path: `perplexity-fetch-url-content/scripts/fetch_url_content.py`
- Use `--require-fetch` when every requested URL must be confirmed
- Do not imply that the API returns full raw HTML

## Verification

One offline-safe local smoke check:

```bash
./scripts/check.sh
```

The script runs:

- `python3 -m py_compile` for `perplexity_common.py` and the direct scripts
- `search_only.py --dry-run --json`
- `fetch_url_content.py --dry-run --json`
- `pro_search.py --help`
- a grep check for key invocation names in README and `.windsurf/`

Live Perplexity requests are intentionally left out of CI and this smoke check because they spend API credits.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `perplexity_search` is not exposed in the session | Use the direct fallback `perplexity_search_only/scripts/search_only.py --json` or the matching Windsurf skill path |
| Cursor cannot see the Perplexity MCP server | Check `.cursor/mcp.json`, confirm `PERPLEXITY_API_KEY`, then inspect with `cursor-agent mcp list` |
| Claude Code cannot see the Perplexity MCP server | Check `.mcp.json`, confirm `PERPLEXITY_API_KEY`, then inspect with `claude mcp list` |
| Claude Code skill does not trigger | Check `.claude/skills/` and restart Claude Code so project skills reload |
| Antigravity does not pick up routing guidance | Check that the workspace includes `AGENTS.md`, then use the repo-local scripts directly |
| `PERPLEXITY_API_KEY` is missing | Check shell env, `~/.codex/config.toml`, `CODEX_HOME/config.toml`, `~/.codeium/windsurf/mcp_config.json` |
| Sonar API billing/auth error | Make sure the Perplexity API balance is funded, not just the Pro subscription |
| A URL is missing from `fetched_urls` | Run Fetch URL mode with `--require-fetch` and inspect `missing_requested_urls` |
| The sandbox blocks network access | Re-run the same script with elevated access instead of switching to another mode |
| CI fails on smoke checks | Run `./scripts/check.sh` locally first, then compare README invocation names and the expected repository structure |

## Cost Notes

Observed cost examples:

- `/perplexity-search`: an example with `4` Search API requests cost **`$0.02`**
- `/perplexity-pro`: a recent run cost **`$0.01819`**
- `/perplexity-fetch-url`: a recent summary run cost **`$0.01894`**
- `/perplexity-research`: one deep research run cost **`$1.38`**

Deep Research is almost always much more expensive than the other modes.

## Repository Structure

```text
perplexity_search_only/              # Codex skill + direct Search API fallback
perplexity-pro-search/               # Codex skill + Sonar Pro Search script
perplexity_deep_research/            # Codex skill for MCP deep research
perplexity-fetch-url-content/        # Codex skill + fetch_url_content script
.windsurf/skills/                    # Windsurf skills
.windsurf/workflows/                 # Windsurf workflows
.windsurf/rules/                     # Shared Windsurf routing rules
.cursor/mcp.json                     # Cursor project MCP config
.cursor/rules/                       # Cursor project rule
.claude/skills/                      # Claude Code project skills
.mcp.json                            # Claude Code project MCP config
AGENTS.md                            # Shared cross-tool routing guidance
scripts/install_to_codex.sh          # Global Codex install
scripts/install_to_windsurf.sh       # Global Windsurf install
scripts/check.sh                     # Offline-safe smoke verification
perplexity_common.py                 # Shared direct-script helpers
skills_manifest.yaml                 # Bundle manifest and install/source-of-truth paths
```

## Notes

- An MCP server being enabled in the UI does not guarantee that its tool is exposed in a specific agent session.
- Search mode includes a direct Search API fallback for that case.
- `skills_manifest.yaml` remains the lightweight source of truth for install paths and Windsurf mappings.
- Cursor MCP project config follows Cursor's documented `.cursor/mcp.json` path and project rules follow `.cursor/rules`.
- Claude Code project MCP config follows Anthropic's documented `.mcp.json` path and project skills follow `.claude/skills/`.
- No `LICENSE` was added in this rollout: this pass is intentionally limited to docs, verification, and repo metadata.
