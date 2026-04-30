#!/bin/zsh
set -euo pipefail

if [[ -z "${PERPLEXITY_API_KEY:-}" ]]; then
  echo "Set PERPLEXITY_API_KEY before running this script."
  echo 'Example: PERPLEXITY_API_KEY="pplx-..." ./scripts/install_to_windsurf.sh'
  exit 1
fi

CONFIG_DIR="$HOME/.codeium/windsurf"
CONFIG_PATH="$CONFIG_DIR/mcp_config.json"
GLOBAL_SKILLS_DIR="$CONFIG_DIR/skills"
GLOBAL_WORKFLOWS_DIR="$CONFIG_DIR/global_workflows"
SCRIPT_DIR="${0:A:h}"
REPO_ROOT="${SCRIPT_DIR:h}"

mkdir -p "$CONFIG_DIR" "$GLOBAL_SKILLS_DIR" "$GLOBAL_WORKFLOWS_DIR"

python3 - "$CONFIG_PATH" <<'PY'
import json
import os
import sys
from pathlib import Path

config_path = Path(sys.argv[1])
api_key = os.environ["PERPLEXITY_API_KEY"]

if config_path.exists():
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Cannot parse {config_path}: {exc}")
else:
    config = {}

config.setdefault("mcpServers", {})
config["mcpServers"]["perplexity"] = {
    "command": "npx",
    "args": ["-y", "@perplexity-ai/mcp-server"],
    "env": {"PERPLEXITY_API_KEY": api_key},
}

config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
PY

echo "Installed Windsurf MCP server config:"
echo "  - $CONFIG_PATH"
cp -R "$REPO_ROOT/.windsurf/skills/perplexity-search" "$GLOBAL_SKILLS_DIR/"
cp -R "$REPO_ROOT/.windsurf/skills/perplexity-research" "$GLOBAL_SKILLS_DIR/"
cp -R "$REPO_ROOT/.windsurf/skills/perplexity-pro" "$GLOBAL_SKILLS_DIR/"
cp -R "$REPO_ROOT/.windsurf/skills/perplexity-fetch-url" "$GLOBAL_SKILLS_DIR/"
cp "$REPO_ROOT/perplexity_search_only/scripts/search_only.py" "$GLOBAL_SKILLS_DIR/perplexity-search/search_only.py"
cp "$REPO_ROOT/perplexity_common.py" "$GLOBAL_SKILLS_DIR/perplexity-search/perplexity_common.py"
cp "$REPO_ROOT/requirements.txt" "$GLOBAL_SKILLS_DIR/perplexity-search/requirements.txt"
cp "$REPO_ROOT/perplexity-pro-search/scripts/pro_search.py" "$GLOBAL_SKILLS_DIR/perplexity-pro/pro_search.py"
cp "$REPO_ROOT/perplexity_common.py" "$GLOBAL_SKILLS_DIR/perplexity-pro/perplexity_common.py"
cp "$REPO_ROOT/requirements.txt" "$GLOBAL_SKILLS_DIR/perplexity-pro/requirements.txt"
cp "$REPO_ROOT/perplexity-fetch-url-content/scripts/fetch_url_content.py" "$GLOBAL_SKILLS_DIR/perplexity-fetch-url/fetch_url_content.py"
cp "$REPO_ROOT/perplexity_common.py" "$GLOBAL_SKILLS_DIR/perplexity-fetch-url/perplexity_common.py"
cp "$REPO_ROOT/requirements.txt" "$GLOBAL_SKILLS_DIR/perplexity-fetch-url/requirements.txt"
cp "$REPO_ROOT/.windsurf/workflows/perplexity-search.md" "$GLOBAL_WORKFLOWS_DIR/"
cp "$REPO_ROOT/.windsurf/workflows/perplexity-research.md" "$GLOBAL_WORKFLOWS_DIR/"
cp "$REPO_ROOT/.windsurf/workflows/perplexity-pro.md" "$GLOBAL_WORKFLOWS_DIR/"
cp "$REPO_ROOT/.windsurf/workflows/perplexity-fetch-url.md" "$GLOBAL_WORKFLOWS_DIR/"

echo "Installed Windsurf skills:"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-search"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-research"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-pro"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-fetch-url"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-search/search_only.py"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-search/perplexity_common.py"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-search/requirements.txt"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-pro/pro_search.py"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-pro/perplexity_common.py"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-pro/requirements.txt"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-fetch-url/fetch_url_content.py"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-fetch-url/perplexity_common.py"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-fetch-url/requirements.txt"
echo "Installed Windsurf workflows:"
echo "  - $GLOBAL_WORKFLOWS_DIR/perplexity-search.md"
echo "  - $GLOBAL_WORKFLOWS_DIR/perplexity-research.md"
echo "  - $GLOBAL_WORKFLOWS_DIR/perplexity-pro.md"
echo "  - $GLOBAL_WORKFLOWS_DIR/perplexity-fetch-url.md"
echo "Restart Windsurf after installation."
