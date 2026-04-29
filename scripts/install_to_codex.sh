#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="${HOME}/.codex/skills"

mkdir -p \
  "$TARGET_DIR/perplexity_search_only" \
  "$TARGET_DIR/perplexity_deep_research" \
  "$TARGET_DIR/perplexity-pro-search"
cp -R "$ROOT_DIR/perplexity_search_only/." "$TARGET_DIR/perplexity_search_only/"
cp -R "$ROOT_DIR/perplexity_deep_research/." "$TARGET_DIR/perplexity_deep_research/"
cp -R "$ROOT_DIR/perplexity-pro-search/." "$TARGET_DIR/perplexity-pro-search/"

echo "Installed:"
echo "  - $TARGET_DIR/perplexity_search_only"
echo "  - $TARGET_DIR/perplexity_deep_research"
echo "  - $TARGET_DIR/perplexity-pro-search"
