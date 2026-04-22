# Perplexity MCP Skills

This bundle contains two explicit Codex skills for working with the Perplexity MCP server:

- `perplexity_search_only` for cheap raw web discovery through `perplexity_search`
- `perplexity_deep_research` for intentionally expensive `perplexity_research`

## Install into Codex

Run:

```bash
./scripts/install_to_codex.sh
```

This copies both skills into `~/.codex/skills/`.

## Layout

- `perplexity_search_only/`
- `perplexity_deep_research/`
- `scripts/install_to_codex.sh`
- `skills_manifest.yaml`

## Invocation

- `$perplexity_search_only <your request>`
- `$perplexity_deep_research <your request>`

## Maintenance

This folder is the editable source bundle inside the Factorix workspace.
If a separate standalone repository exists, sync this bundle into that repository after changes.
