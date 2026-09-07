#!/usr/bin/env python3
"""Fetch daily top headlines from NewsAPI and write data/daily-news.json."""
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

CATEGORIES = ["technology", "business", "sports"]
PAGE_SIZE = 5
API_URL = "https://newsapi.org/v2/top-headlines"
OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "daily-news.json"
)


def is_removed(article):
    """NewsAPI returns syndication-blocked articles as placeholders. Filter them out."""
    if article.get("title") == "[Removed]":
        return True
    if (article.get("source") or {}).get("name") == "[Removed]":
        return True
    if article.get("url") == "https://removed.com":
        return True
    return False


def map_article(article):
    return {
        "title": article.get("title"),
        "description": article.get("description"),
        "url": article.get("url"),
        "source": (article.get("source") or {}).get("name"),
        "publishedAt": article.get("publishedAt"),
        "image": article.get("urlToImage"),
    }


def fetch_category(category, api_key):
    url = f"{API_URL}?country=us&category={category}&pageSize={PAGE_SIZE}"
    req = urllib.request.Request(url, headers={"X-Api-Key": api_key})
    with urllib.request.urlopen(req, timeout=15) as response:
        body = json.loads(response.read().decode("utf-8"))

    if body.get("status") != "ok":
        raise RuntimeError(f"NewsAPI error for category '{category}': {body}")

    articles = [a for a in body.get("articles", []) if not is_removed(a)]
    if not articles:
        raise RuntimeError(f"No usable articles returned for category '{category}'")

    return [map_article(a) for a in articles]


def build_payload(api_key):
    categories = {category: fetch_category(category, api_key) for category in CATEGORIES}
    return {
        "updated": datetime.now(timezone.utc).date().isoformat(),
        "categories": categories,
    }


def main():
    api_key = os.environ.get("NEWS_API_KEY")
    if not api_key:
        print("NEWS_API_KEY environment variable is not set", file=sys.stderr)
        return 1

    try:
        payload = build_payload(api_key)
    except (RuntimeError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"Failed to fetch daily news: {exc}", file=sys.stderr)
        return 1

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
