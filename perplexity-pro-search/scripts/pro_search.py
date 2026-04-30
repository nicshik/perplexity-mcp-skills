#!/usr/bin/env python3
"""Run Perplexity Sonar Pro with Pro Search enabled.

This script calls the official Sonar API with:
- stream=true
- stream_mode=concise
- web_search_options.search_type=pro
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
for helper_dir in (CURRENT_DIR, CURRENT_DIR.parent, CURRENT_DIR.parent.parent):
    if (helper_dir / "perplexity_common.py").exists():
        sys.path.insert(0, str(helper_dir))
        break

from perplexity_common import build_json_request, open_request, read_query


API_URL = "https://api.perplexity.ai/v1/sonar"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Perplexity Pro Search (Sonar Pro + search_type=pro)."
    )
    parser.add_argument("query", nargs="?", help="User query. If omitted, stdin is used.")
    parser.add_argument(
        "--system",
        default="Answer concisely and cite the strongest current web sources.",
        help="Optional system prompt.",
    )
    parser.add_argument(
        "--context-size",
        choices=("low", "medium", "high"),
        default="medium",
        help="Web search context size.",
    )
    parser.add_argument(
        "--recency",
        choices=("hour", "day", "week", "month", "year"),
        help="Filter search results by recency.",
    )
    parser.add_argument(
        "--domain",
        action="append",
        default=[],
        help="Allowlist or denylist domain/url filter. Repeatable. Use -domain.com to exclude.",
    )
    parser.add_argument(
        "--language",
        action="append",
        default=[],
        help="Filter search result languages with ISO 639-1 codes. Repeatable.",
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=("minimal", "low", "medium", "high"),
        help="Optional Sonar reasoning effort.",
    )
    parser.add_argument(
        "--show-reasoning",
        action="store_true",
        help="Include reasoning steps in human-readable output.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON instead of formatted text.",
    )
    return parser.parse_args()


def build_payload(args: argparse.Namespace, query: str) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": args.system},
            {"role": "user", "content": query},
        ],
        "stream": True,
        "stream_mode": "concise",
        "web_search_options": {
            "search_type": "pro",
            "search_context_size": args.context_size,
        },
    }
    if args.recency:
        payload["search_recency_filter"] = args.recency
    if args.domain:
        payload["search_domain_filter"] = args.domain
    if args.language:
        payload["search_language_filter"] = args.language
    if args.reasoning_effort:
        payload["reasoning_effort"] = args.reasoning_effort
    return payload


def stream_request(payload: dict[str, Any]) -> dict[str, Any]:
    request = build_json_request(API_URL, payload, accept="text/event-stream")

    result: dict[str, Any] = {
        "content": "",
        "search_results": [],
        "usage": None,
        "reasoning_steps": [],
        "raw_objects_seen": [],
    }

    with open_request(request) as response:
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
                for choice in chunk.get("choices", []):
                    delta = choice.get("delta", {})
                    for step in delta.get("reasoning_steps", []) or []:
                        result["reasoning_steps"].append(step)

            elif obj == "chat.reasoning.done":
                if chunk.get("search_results"):
                    result["search_results"] = chunk["search_results"]

            elif obj == "chat.completion.chunk":
                for choice in chunk.get("choices", []):
                    delta = choice.get("delta", {})
                    content = delta.get("content")
                    if content:
                        result["content"] += content

            elif obj == "chat.completion.done":
                if chunk.get("search_results"):
                    result["search_results"] = chunk["search_results"]
                if chunk.get("usage"):
                    result["usage"] = chunk["usage"]

    return result


def print_human(result: dict[str, Any], show_reasoning: bool) -> None:
    print(result["content"].strip())

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
            if thought:
                print(f"- {thought}")


def main() -> int:
    args = parse_args()
    query = read_query(args.query)
    payload = build_payload(args, query)
    result = stream_request(payload)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result, args.show_reasoning)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
