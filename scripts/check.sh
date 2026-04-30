#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$ROOT_DIR"

python3 -m py_compile \
  perplexity_common.py \
  perplexity_search_only/scripts/search_only.py \
  perplexity-pro-search/scripts/pro_search.py \
  perplexity-fetch-url-content/scripts/fetch_url_content.py

python3 perplexity_search_only/scripts/search_only.py \
  "Perplexity MCP server documentation" \
  --dry-run \
  --json >/dev/null

python3 perplexity-fetch-url-content/scripts/fetch_url_content.py \
  --dry-run \
  --json \
  https://docs.perplexity.ai/docs/sonar/pro-search/tools >/dev/null

python3 perplexity-pro-search/scripts/pro_search.py --help >/dev/null

grep -R -q '\$perplexity_search_only' README.md README.en.md .windsurf
grep -R -q '\$perplexity-pro-search' README.md README.en.md .windsurf
grep -R -q '\$perplexity_deep_research' README.md README.en.md .windsurf
grep -R -q '\$perplexity-fetch-url-content' README.md README.en.md .windsurf
grep -R -q '@perplexity-search' README.md README.en.md .windsurf
grep -R -q '@perplexity-pro' README.md README.en.md .windsurf
grep -R -q '@perplexity-research' README.md README.en.md .windsurf
grep -R -q '@perplexity-fetch-url' README.md README.en.md .windsurf
grep -R -q '/perplexity-search' README.md README.en.md .windsurf
grep -R -q '/perplexity-pro' README.md README.en.md .windsurf
grep -R -q '/perplexity-research' README.md README.en.md .windsurf
grep -R -q '/perplexity-fetch-url' README.md README.en.md .windsurf

echo "Smoke checks passed."
