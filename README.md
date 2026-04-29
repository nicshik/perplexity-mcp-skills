# Perplexity MCP Skills

This bundle contains three explicit Codex skills for working with Perplexity search modes:

- `perplexity_search_only` for cheap raw web discovery through `perplexity_search`
- `perplexity_deep_research` for intentionally expensive `perplexity_research`
- `perplexity-pro-search` for direct Pro Search API calls through `sonar-pro` with `search_type=pro`

## Install into Codex

Run:

```bash
./scripts/install_to_codex.sh
```

This copies all three skills into `~/.codex/skills/`.

## Layout

- `perplexity_search_only/`
- `perplexity_deep_research/`
- `perplexity-pro-search/`
- `scripts/install_to_codex.sh`
- `skills_manifest.yaml`

## Invocation

- `$perplexity_search_only <your request>`
- `$perplexity_deep_research <your request>`
- `$perplexity-pro-search <your request>`

## Maintenance

This folder is the editable source bundle inside the Factorix workspace.
If a separate standalone repository exists, sync this bundle into that repository after changes.
