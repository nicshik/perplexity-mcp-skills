#!/usr/bin/env python3
"""Run low-cost Perplexity Search API queries without answer synthesis."""

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


API_URL = "https://api.perplexity.ai/search"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run cheap Perplexity Search API lookups without answer synthesis."
    )
    parser.add_argument("query", nargs="?", help="Search query. If omitted, stdin is used.")
    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="Maximum number of results to return (1-5). Default: 5.",
    )
    parser.add_argument(
        "--max-tokens-per-page",
        type=int,
        default=512,
        help="Maximum extracted tokens per page. Default: 512.",
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
        "--country",
        help="Optional ISO 3166-1 alpha-2 country code.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON instead of formatted text.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request payload and exit without calling the API.",
    )
    return parser.parse_args()


def build_payload(args: argparse.Namespace, query: str) -> dict[str, Any]:
    if not 1 <= args.max_results <= 5:
        raise SystemExit("--max-results must be between 1 and 5.")

    payload: dict[str, Any] = {
        "query": query,
        "max_results": args.max_results,
        "max_tokens_per_page": args.max_tokens_per_page,
    }
    if args.recency:
        payload["search_recency_filter"] = args.recency
    if args.domain:
        payload["search_domain_filter"] = args.domain
    if args.language:
        payload["search_language_filter"] = args.language
    if args.country:
        payload["country"] = args.country.upper()
    return payload


def run_search(payload: dict[str, Any]) -> dict[str, Any]:
    request = build_json_request(API_URL, payload, accept="application/json")
    with open_request(request) as response:
        return json.loads(response.read().decode("utf-8"))


def print_human(result: dict[str, Any]) -> None:
    results = result.get("results") or []
    if not results:
        print("No results.")
        return

    for item in results:
        title = item.get("title") or "(untitled)"
        url = item.get("url") or ""
        date = item.get("date") or item.get("last_updated") or ""
        snippet = item.get("snippet") or ""
        suffix = f" [{date}]" if date else ""
        print(f"- {title}{suffix}")
        if url:
            print(f"  {url}")
        if snippet:
            print(f"  {snippet}")


def main() -> int:
    args = parse_args()
    query = read_query(args.query)
    payload = build_payload(args, query)

    if args.dry_run:
        print(json.dumps({"query": query, "payload": payload}, ensure_ascii=False, indent=2))
        return 0

    result = run_search(payload)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
