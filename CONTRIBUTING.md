# Contributing

## Scope

This repository is intentionally narrow: it packages Perplexity modes for Codex and Windsurf without hiding cost, depth, or invocation semantics.

Prefer changes that keep these guarantees explicit:

- Search only stays separate from Pro Search and Deep Research.
- Deep Research remains MCP-only unless the repository explicitly adds a new supported path.
- Fetch URL keeps its current `fetch_url_content` semantics and does not claim raw HTML extraction.

## Before Opening A PR

1. Keep invocation names stable:
   - Codex: `$perplexity_search_only`, `$perplexity-pro-search`, `$perplexity_deep_research`, `$perplexity-fetch-url-content`
   - Windsurf: `@perplexity-search`, `@perplexity-pro`, `@perplexity-research`, `@perplexity-fetch-url`
   - Workflows: `/perplexity-search`, `/perplexity-pro`, `/perplexity-research`, `/perplexity-fetch-url`
2. Run the local smoke checks:

```bash
./scripts/check.sh
```

3. If you touch direct scripts, keep verification offline-safe unless the change explicitly requires live API validation.
4. If you change docs, keep `README.md`, `README.en.md`, `.windsurf/`, and `skills_manifest.yaml` aligned.

## Contribution Style

- Keep mode boundaries explicit.
- Prefer small, reviewable commits.
- Update docs and examples in the same change when behavior or positioning changes.
- Do not add hidden fallbacks that silently switch one mode into another.

## Out Of Scope By Default

- Automatic license selection
- Secret-dependent CI checks
- Changes that make Deep Research or Fetch URL behave like generic search
