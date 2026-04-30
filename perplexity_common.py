#!/usr/bin/env python3
"""Shared helpers for direct Perplexity API scripts."""

from __future__ import annotations

import json
import os
import ssl
import sys
from pathlib import Path
import urllib.error
import urllib.request

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

try:
    import certifi
except ModuleNotFoundError:  # pragma: no cover
    certifi = None


def read_query(arg_query: str | None) -> str:
    if arg_query:
        return arg_query.strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    raise SystemExit("Query is required as an argument or via stdin.")


def load_api_key_from_codex_config() -> str | None:
    if tomllib is None:
        return None

    codex_home = Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()
    config_path = codex_home / "config.toml"
    if not config_path.exists():
        return None

    try:
        with config_path.open("rb") as handle:
            config = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError):
        return None

    return (
        config.get("mcp_servers", {})
        .get("perplexity", {})
        .get("env", {})
        .get("PERPLEXITY_API_KEY")
    )


def load_api_key_from_windsurf_config() -> str | None:
    config_path = Path("~/.codeium/windsurf/mcp_config.json").expanduser()
    if not config_path.exists():
        return None

    try:
        with config_path.open("r", encoding="utf-8") as handle:
            config = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None

    servers = config.get("mcpServers", {})
    for server_name in ("perplexity", "perplexity-mcp"):
        api_key = (
            servers.get(server_name, {})
            .get("env", {})
            .get("PERPLEXITY_API_KEY")
        )
        if api_key:
            return api_key
    return None


def resolve_api_key() -> str:
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if api_key:
        return api_key

    api_key = load_api_key_from_codex_config()
    if api_key:
        return api_key

    api_key = load_api_key_from_windsurf_config()
    if api_key:
        return api_key

    raise SystemExit(
        "PERPLEXITY_API_KEY was not found in the shell environment, ~/.codex/config.toml "
        "(CODEX_HOME/config.toml), or ~/.codeium/windsurf/mcp_config.json."
    )


def build_ssl_context() -> ssl.SSLContext:
    if certifi is not None:
        return ssl.create_default_context(cafile=certifi.where())
    return ssl.create_default_context()


def format_connection_error(exc: urllib.error.URLError) -> str:
    reason = getattr(exc, "reason", None)
    if isinstance(reason, ssl.SSLCertVerificationError):
        return (
            f"Perplexity API connection error: {exc}\n"
            "SSL certificate verification failed. Install `certifi` "
            "(for example, `python3 -m pip install certifi`), install repository "
            "dependencies with `python3 -m pip install -r requirements.txt` from "
            "the repository root, or configure your Python installation's CA certificates."
        )
    return f"Perplexity API connection error: {exc}"


def build_json_request(
    api_url: str,
    payload: dict,
    *,
    accept: str,
) -> urllib.request.Request:
    body = json.dumps(payload).encode("utf-8")
    return urllib.request.Request(
        api_url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {resolve_api_key()}",
            "Content-Type": "application/json",
            "Accept": accept,
        },
    )


def open_request(request: urllib.request.Request):
    try:
        return urllib.request.urlopen(request, context=build_ssl_context())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Perplexity API HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(format_connection_error(exc)) from exc
