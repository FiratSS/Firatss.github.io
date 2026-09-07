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
