#!/usr/bin/env python3
"""Read specific URLs through Perplexity Sonar Pro fetch_url_content.

Perplexity exposes fetch_url_content as an automatic Pro Search built-in tool,
not as a direct HTTP endpoint. This script sends a strict Sonar Pro prompt and
then inspects streamed reasoning_steps to report which URLs were fetched.
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
from pathlib import Path
from typing import Any
from urllib.parse import urlparse, urlunparse
import urllib.error
import urllib.request

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


API_URL = "https://api.perplexity.ai/v1/sonar"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read specific URLs through Perplexity Sonar Pro fetch_url_content."
    )
    parser.add_argument("urls", nargs="+", help="URL(s) to fetch and read.")
    parser.add_argument(
        "--question",
        help="Optional focused question to answer from the supplied URL content.",
    )
    parser.add_argument(
        "--mode",
        choices=("max-text", "qa", "summary"),
        default="max-text",
        help="Extraction mode. Defaults to max-text.",
    )
    parser.add_argument(
        "--context-size",
        choices=("low", "medium", "high"),
        default="high",
        help="Web search context size.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON instead of formatted text.",
    )
    parser.add_argument(
        "--show-reasoning",
        action="store_true",
        help="Include reasoning steps in human-readable output.",
    )
    parser.add_argument(
        "--require-fetch",
        action="store_true",
        help="Exit non-zero if any requested URL is not confirmed in fetch_url_content reasoning steps.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request payload and exit without calling the API.",
    )
    return parser.parse_args()


def validate_urls(urls: list[str]) -> list[str]:
    normalized_urls = []
    for raw_url in urls:
        parsed = urlparse(raw_url.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise SystemExit(f"Invalid URL: {raw_url}")
        normalized_urls.append(urlunparse(parsed))
    return normalized_urls


def normalize_url_for_compare(url: str) -> str:
    parsed = urlparse(url.strip())
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/") or "/"
    return urlunparse((scheme, netloc, path, "", parsed.query, ""))


def build_user_prompt(urls: list[str], mode: str, question: str | None) -> str:
    url_lines = "\n".join(f"- {url}" for url in urls)
    prompt_parts = [
        "Use Pro Search built-in fetch_url_content for each URL below if available.",
        "Do not answer from snippets alone when URL content can be fetched.",
        "If any URL cannot be fetched, say that clearly and use only what is available.",
        "",
        "URLs:",
        url_lines,
        "",
    ]

    if mode == "max-text":
        prompt_parts.extend(
            [
                "Task: extract the maximum useful page content you can from the fetched URL content.",
                "Preserve the source structure with headings, sections, lists, tables, key fields, dates, names, and important quoted fragments where useful.",
                "Do not claim to provide raw HTML or a guaranteed complete verbatim dump.",
            ]
        )
    elif mode == "qa":
        prompt_parts.extend(
            [
                "Task: answer the question strictly from the fetched URL content.",
                "If the fetched content does not contain the answer, say so.",
            ]
        )
    else:
        prompt_parts.extend(
            [
                "Task: summarize the fetched URL content concisely.",
                "Include the most important facts, entities, dates, and source-specific caveats.",
            ]
        )

    if question:
        prompt_parts.extend(["", f"Question: {question}"])

    return "\n".join(prompt_parts)


def build_payload(args: argparse.Namespace, urls: list[str]) -> dict[str, Any]:
    system_prompt = (
        "You read specific user-supplied URLs using Pro Search built-in URL content fetching. "
        "Prefer fetched page content over search snippets. Be explicit about fetch failures."
    )
    return {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": build_user_prompt(urls, args.mode, args.question),
            },
        ],
        "stream": True,
        "stream_mode": "concise",
        "web_search_options": {
            "search_type": "pro",
            "search_context_size": args.context_size,
        },
    }


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
    return ssl.create_default_context()


def stream_request(payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {resolve_api_key()}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
    )

    result: dict[str, Any] = {
        "content": "",
        "search_results": [],
        "usage": None,
        "reasoning_steps": [],
        "raw_objects_seen": [],
    }

    try:
        with urllib.request.urlopen(request, context=build_ssl_context()) as response:
            for raw_line in response:
                line = raw_line.decode("utf-8").strip()
                if not line or not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break

                chunk = json.loads(data)
                obj = chunk.get("object")
                if obj:
                    result["raw_objects_seen"].append(obj)

                if obj == "chat.reasoning":
                    append_reasoning_steps(result, chunk)
                elif obj == "chat.reasoning.done":
                    append_reasoning_steps_from_message(result, chunk)
                    if chunk.get("search_results"):
                        result["search_results"] = chunk["search_results"]
                    if chunk.get("usage"):
                        result["usage"] = chunk["usage"]
                elif obj == "chat.completion.chunk":
                    for choice in chunk.get("choices", []):
                        delta = choice.get("delta", {})
                        content = delta.get("content")
                        if content:
                            result["content"] += content
                elif obj == "chat.completion.done":
                    append_reasoning_steps_from_message(result, chunk)
                    if chunk.get("search_results"):
                        result["search_results"] = chunk["search_results"]
                    if chunk.get("usage"):
                        result["usage"] = chunk["usage"]
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Perplexity API HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Perplexity API connection error: {exc}") from exc

    return result


def append_reasoning_steps(result: dict[str, Any], chunk: dict[str, Any]) -> None:
    for choice in chunk.get("choices", []):
        delta = choice.get("delta", {})
        for step in delta.get("reasoning_steps", []) or []:
            result["reasoning_steps"].append(step)


def append_reasoning_steps_from_message(result: dict[str, Any], chunk: dict[str, Any]) -> None:
    for choice in chunk.get("choices", []):
        message = choice.get("message", {})
        for step in message.get("reasoning_steps", []) or []:
            if step not in result["reasoning_steps"]:
                result["reasoning_steps"].append(step)


def extract_fetched_urls(reasoning_steps: list[dict[str, Any]]) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()

    for step in reasoning_steps:
        if step.get("type") != "fetch_url_content":
            continue
        fetch_data = step.get("fetch_url_content") or {}
        for item in fetch_data.get("contents", []) or []:
            url = item.get("url")
            if not url:
                continue
            normalized = normalize_url_for_compare(url)
            if normalized not in seen:
                seen.add(normalized)
                urls.append(url)

    return urls


def find_missing_requested_urls(requested_urls: list[str], fetched_urls: list[str]) -> list[str]:
    fetched_normalized = {normalize_url_for_compare(url) for url in fetched_urls}
    missing = []
    for url in requested_urls:
        if normalize_url_for_compare(url) not in fetched_normalized:
            missing.append(url)
    return missing


def enrich_result(result: dict[str, Any], requested_urls: list[str], payload: dict[str, Any]) -> None:
    fetched_urls = extract_fetched_urls(result.get("reasoning_steps") or [])
    result["fetched_urls"] = fetched_urls
    result["missing_requested_urls"] = find_missing_requested_urls(requested_urls, fetched_urls)
    result["payload"] = payload


def print_human(result: dict[str, Any], show_reasoning: bool) -> None:
    print(result["content"].strip())

    fetched_urls = result.get("fetched_urls") or []
    missing_urls = result.get("missing_requested_urls") or []
    print("\nFetch verification:")
    if fetched_urls:
        for url in fetched_urls:
            print(f"- fetched: {url}")
    else:
        print("- no fetch_url_content steps were reported")
    for url in missing_urls:
        print(f"- missing: {url}")

    sources = result.get("search_results") or []
    if sources:
        print("\nSources:")
        for item in sources[:10]:
            title = item.get("title") or "(untitled)"
            url = item.get("url") or ""
            date = item.get("date") or item.get("last_updated") or ""
            suffix = f" [{date}]" if date else ""
            print(f"- {title}{suffix}")
            if url:
                print(f"  {url}")

    usage = result.get("usage")
    if usage:
        total_cost = ((usage.get("cost") or {}).get("total_cost"))
        search_context_size = usage.get("search_context_size")
        print("\nUsage:")
        print(f"- total_tokens: {usage.get('total_tokens')}")
        print(f"- num_search_queries: {usage.get('num_search_queries')}")
        if search_context_size:
            print(f"- search_context_size: {search_context_size}")
        if total_cost is not None:
            print(f"- total_cost: {total_cost}")

    if show_reasoning and result.get("reasoning_steps"):
        print("\nReasoning steps:")
        for step in result["reasoning_steps"]:
            thought = step.get("thought")
            step_type = step.get("type")
            prefix = f"[{step_type}] " if step_type else ""
            if thought:
                print(f"- {prefix}{thought}")


def main() -> int:
    args = parse_args()
    if args.mode == "qa" and not args.question:
        raise SystemExit("--question is required with --mode qa.")

    requested_urls = validate_urls(args.urls)
    payload = build_payload(args, requested_urls)

    if args.dry_run:
        dry_run_result = {
            "requested_urls": requested_urls,
            "payload": payload,
        }
        print(json.dumps(dry_run_result, ensure_ascii=False, indent=2))
        return 0

    result = stream_request(payload)
    enrich_result(result, requested_urls, payload)

    if args.require_fetch and result["missing_requested_urls"]:
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_human(result, args.show_reasoning)
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result, args.show_reasoning)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
