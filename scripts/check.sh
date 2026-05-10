#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$ROOT_DIR"

required_files=(
  package.json
  package-lock.json
  tsconfig.json
  README.md
  README.ru.md
  LICENSE
  docs/releasing.md
  AGENTS.md
  skills_manifest.yaml
  .github/workflows/ci.yml
  .github/workflows/release.yml
  .cursor/mcp.json
  .cursor/rules/perplexity.mdc
  .mcp.json
  .claude/skills/perplexity-search-only/SKILL.md
  .claude/skills/perplexity-pro-search/SKILL.md
  .claude/skills/perplexity-deep-research/SKILL.md
  .claude/skills/perplexity-fetch-url/SKILL.md
  perplexity_search_only/SKILL.md
  perplexity-pro-search/SKILL.md
  perplexity_deep_research/SKILL.md
  perplexity-fetch-url-content/SKILL.md
  perplexity_search_only/agents/openai.yaml
  perplexity-pro-search/agents/openai.yaml
  perplexity_deep_research/agents/openai.yaml
  perplexity-fetch-url-content/agents/openai.yaml
  perplexity_search_only/references/prompt_recipes.md
  perplexity-pro-search/references/prompt_recipes.md
  perplexity_deep_research/references/prompt_recipes.md
  perplexity-fetch-url-content/references/prompt_recipes.md
  perplexity_search_only/scripts/search_only.py
  perplexity-pro-search/scripts/pro_search.py
  perplexity-fetch-url-content/scripts/fetch_url_content.py
  src/cli.ts
  src/install.ts
  src/doctor.ts
  src/sync.ts
  src/uninstall.ts
)

for path in "${required_files[@]}"; do
  test -f "$path"
done

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

npm run typecheck >/dev/null
npm run build >/dev/null
node dist/cli.js --help >/dev/null
node dist/cli.js install all --dry-run --no-key --yes >/dev/null
node dist/cli.js doctor --target all --offline --json >/dev/null || test "$?" -eq 1

grep -q 'Codex' README.md
grep -q 'Windsurf' README.md
grep -q 'Cursor' README.md
grep -q 'Claude Code' README.md
grep -q 'Antigravity' README.md
grep -q 'Codex' README.ru.md
grep -q 'Windsurf' README.ru.md
grep -q 'Cursor' README.ru.md
grep -q 'Claude Code' README.ru.md
grep -q 'Antigravity' README.ru.md
grep -q 'What To Pick In 30 Seconds' README.md
grep -q 'Что выбрать за 30 секунд' README.ru.md
grep -q 'Compatibility Matrix' README.md
grep -q 'Матрица совместимости' README.ru.md
grep -q 'Troubleshooting' README.md
grep -q 'Troubleshooting' README.ru.md
grep -q 'npx perplexity-mcp-skills install' README.md
grep -q 'npx perplexity-mcp-skills install' README.ru.md

grep -R -q '\$perplexity_search_only' README.md README.ru.md .windsurf
grep -R -q '\$perplexity-pro-search' README.md README.ru.md .windsurf
grep -R -q '\$perplexity_deep_research' README.md README.ru.md .windsurf
grep -R -q '\$perplexity-fetch-url-content' README.md README.ru.md .windsurf
grep -R -q '@perplexity-search' README.md README.ru.md .windsurf
grep -R -q '@perplexity-pro' README.md README.ru.md .windsurf
grep -R -q '@perplexity-research' README.md README.ru.md .windsurf
grep -R -q '@perplexity-fetch-url' README.md README.ru.md .windsurf
grep -R -q '/perplexity-search' README.md README.ru.md .windsurf
grep -R -q '/perplexity-pro' README.md README.ru.md .windsurf
grep -R -q '/perplexity-research' README.md README.ru.md .windsurf
grep -R -q '/perplexity-fetch-url' README.md README.ru.md .windsurf

grep -q 'purpose: "Search only mode through Perplexity MCP with direct Search API fallback"' skills_manifest.yaml
grep -q 'purpose: "Deep Research mode through Perplexity MCP"' skills_manifest.yaml
grep -q 'purpose: "Pro Search mode through Sonar Pro"' skills_manifest.yaml
grep -q 'purpose: "Fetch URL mode through Sonar Pro fetch_url_content"' skills_manifest.yaml
grep -q 'cursor_mcp: ".cursor/mcp.json"' skills_manifest.yaml
grep -q 'claude_mcp: ".mcp.json"' skills_manifest.yaml
grep -q 'shared_agent_rules: "AGENTS.md"' skills_manifest.yaml

echo "Smoke checks passed."
