#!/bin/zsh
set -euo pipefail

if [[ -z "${PERPLEXITY_API_KEY:-}" ]]; then
  echo "Set PERPLEXITY_API_KEY before running this script."
  echo 'Example: PERPLEXITY_API_KEY="pplx-..." ./scripts/install_to_windsurf.sh'
  exit 1
fi

CONFIG_DIR="$HOME/.codeium/windsurf"
CONFIG_PATH="$CONFIG_DIR/mcp_config.json"

mkdir -p "$CONFIG_DIR"

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
echo "Restart Windsurf after installation."
