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
cp "$REPO_ROOT/.windsurf/workflows/perplexity-search.md" "$GLOBAL_WORKFLOWS_DIR/"
cp "$REPO_ROOT/.windsurf/workflows/perplexity-research.md" "$GLOBAL_WORKFLOWS_DIR/"
cp "$REPO_ROOT/.windsurf/workflows/perplexity-pro.md" "$GLOBAL_WORKFLOWS_DIR/"
cp "$REPO_ROOT/.windsurf/workflows/perplexity-fetch-url.md" "$GLOBAL_WORKFLOWS_DIR/"

echo "Installed Windsurf skills:"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-search"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-research"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-pro"
echo "  - $GLOBAL_SKILLS_DIR/perplexity-fetch-url"
echo "Installed Windsurf workflows:"
echo "  - $GLOBAL_WORKFLOWS_DIR/perplexity-search.md"
echo "  - $GLOBAL_WORKFLOWS_DIR/perplexity-research.md"
echo "  - $GLOBAL_WORKFLOWS_DIR/perplexity-pro.md"
echo "  - $GLOBAL_WORKFLOWS_DIR/perplexity-fetch-url.md"
echo "Restart Windsurf after installation."
