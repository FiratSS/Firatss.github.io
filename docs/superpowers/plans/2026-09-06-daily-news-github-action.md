# Daily News GitHub Action Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the manual/local n8n daily news refresh with a self-contained GitHub Actions workflow that fetches NewsAPI headlines and commits `data/daily-news.json` automatically.

**Architecture:** A stdlib-only Python script (`scripts/fetch_news.py`) fetches 3 categories from NewsAPI, filters NewsAPI's "[Removed]" placeholder articles, and writes `data/daily-news.json` in the existing schema. A GitHub Actions workflow (`.github/workflows/daily-news.yml`) runs the script daily on a cron schedule (plus manual `workflow_dispatch`) and commits the result using the built-in `GITHUB_TOKEN`.

**Tech Stack:** Python 3 standard library only (`urllib.request`, `json`, `unittest`), GitHub Actions (`actions/checkout@v4`, `actions/setup-python@v5`), NewsAPI.org `top-headlines` endpoint.

**Spec:** `docs/superpowers/specs/2026-09-06-daily-news-github-action-design.md`

---

## Chunk 1: Fetch script, tests, and workflow

### Task 1: `is_removed` filter — script skeleton + first function

**Files:**
- Create: `scripts/fetch_news.py`
- Create: `scripts/test_fetch_news.py`

- [ ] **Step 1: Write the failing test**

```python
# scripts/test_fetch_news.py
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import fetch_news


class TestIsRemoved(unittest.TestCase):
    def test_removed_title(self):
        self.assertTrue(fetch_news.is_removed({"title": "[Removed]"}))

    def test_removed_source_name(self):
        self.assertTrue(fetch_news.is_removed({"source": {"name": "[Removed]"}}))

    def test_removed_url(self):
        self.assertTrue(fetch_news.is_removed({"url": "https://removed.com"}))

    def test_normal_article_not_removed(self):
        article = {
            "title": "Real headline",
            "source": {"name": "BBC"},
            "url": "https://bbc.com/x",
        }
        self.assertFalse(fetch_news.is_removed(article))

    def test_missing_source_does_not_crash(self):
        self.assertFalse(fetch_news.is_removed({"title": "Real headline"}))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest scripts.test_fetch_news -v` (from repo root)
Expected: FAIL/ERROR — `fetch_news.py` doesn't exist yet (`ModuleNotFoundError`)

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/fetch_news.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest scripts.test_fetch_news -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch_news.py scripts/test_fetch_news.py
git commit -m "Add is_removed filter for NewsAPI placeholder articles"
```

---

### Task 2: `map_article` — field mapping to existing schema

**Files:**
- Modify: `scripts/fetch_news.py`
- Modify: `scripts/test_fetch_news.py`

- [ ] **Step 1: Write the failing test**

Add to `scripts/test_fetch_news.py` (above the `if __name__ == "__main__":` line):

```python
class TestMapArticle(unittest.TestCase):
    def test_maps_expected_fields(self):
        article = {
            "title": "T",
            "description": "D",
            "url": "https://x.com",
            "source": {"id": "bbc-news", "name": "BBC"},
            "publishedAt": "2026-01-01T00:00:00Z",
            "urlToImage": "https://x.com/img.jpg",
        }
        self.assertEqual(
            fetch_news.map_article(article),
            {
                "title": "T",
                "description": "D",
                "url": "https://x.com",
                "source": "BBC",
                "publishedAt": "2026-01-01T00:00:00Z",
                "image": "https://x.com/img.jpg",
            },
        )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest scripts.test_fetch_news -v`
Expected: FAIL — `AttributeError: module 'fetch_news' has no attribute 'map_article'`

- [ ] **Step 3: Write minimal implementation**

Add to `scripts/fetch_news.py` (after `is_removed`):

```python
def map_article(article):
    return {
        "title": article.get("title"),
        "description": article.get("description"),
        "url": article.get("url"),
        "source": (article.get("source") or {}).get("name"),
        "publishedAt": article.get("publishedAt"),
        "image": article.get("urlToImage"),
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest scripts.test_fetch_news -v`
Expected: PASS (6 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch_news.py scripts/test_fetch_news.py
git commit -m "Add map_article to match daily-news.json schema"
```

---

### Task 3: `fetch_category` — HTTP call, timeout, filtering, empty-result failure

**Files:**
- Modify: `scripts/fetch_news.py`
- Modify: `scripts/test_fetch_news.py`

- [ ] **Step 1: Write the failing test**

Add to `scripts/test_fetch_news.py`:

```python
from unittest.mock import MagicMock, patch


class TestFetchCategory(unittest.TestCase):
    def _mock_response(self, body_dict):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(body_dict).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        return mock_response

    @patch("fetch_news.urllib.request.urlopen")
    def test_filters_removed_and_maps_remaining(self, mock_urlopen):
        body = {
            "status": "ok",
            "articles": [
                {"title": "[Removed]", "url": "https://removed.com"},
                {
                    "title": "Real",
                    "description": "d",
                    "url": "https://x.com",
                    "source": {"name": "BBC"},
                    "publishedAt": "p",
                    "urlToImage": "i",
                },
            ],
        }
        mock_urlopen.return_value = self._mock_response(body)

        result = fetch_news.fetch_category("technology", "fake-key")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Real")
        # Confirm timeout is passed through to urlopen
        _, kwargs = mock_urlopen.call_args
        self.assertEqual(kwargs.get("timeout"), 15)

    @patch("fetch_news.urllib.request.urlopen")
    def test_raises_when_all_articles_removed(self, mock_urlopen):
        body = {"status": "ok", "articles": [{"title": "[Removed]"}]}
        mock_urlopen.return_value = self._mock_response(body)

        with self.assertRaises(RuntimeError):
            fetch_news.fetch_category("technology", "fake-key")

    @patch("fetch_news.urllib.request.urlopen")
    def test_raises_on_non_ok_status(self, mock_urlopen):
        body = {"status": "error", "code": "apiKeyInvalid", "message": "bad key"}
        mock_urlopen.return_value = self._mock_response(body)

        with self.assertRaises(RuntimeError):
            fetch_news.fetch_category("technology", "fake-key")
```

Add `import json` to the top of `scripts/test_fetch_news.py` if not already present (it is needed here for `json.dumps`).

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest scripts.test_fetch_news -v`
Expected: FAIL — `AttributeError: module 'fetch_news' has no attribute 'fetch_category'`

- [ ] **Step 3: Write minimal implementation**

Add to `scripts/fetch_news.py` (after `map_article`):

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest scripts.test_fetch_news -v`
Expected: PASS (9 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch_news.py scripts/test_fetch_news.py
git commit -m "Add fetch_category with 15s timeout and empty-result guard"
```

---

### Task 4: `build_payload` + `main` — assembly, UTC date, file write, error exit codes

**Files:**
- Modify: `scripts/fetch_news.py`
- Modify: `scripts/test_fetch_news.py`

- [ ] **Step 1: Write the failing test**

Add to `scripts/test_fetch_news.py`:

```python
import tempfile


class TestBuildPayload(unittest.TestCase):
    @patch("fetch_news.fetch_category")
    @patch("fetch_news.datetime")
    def test_builds_payload_for_all_categories(self, mock_datetime, mock_fetch_category):
        from datetime import date

        mock_datetime.now.return_value.date.return_value = date(2026, 1, 15)
        mock_fetch_category.side_effect = lambda category, key: [{"title": category}]

        payload = fetch_news.build_payload("fake-key")

        self.assertEqual(payload["updated"], "2026-01-15")
        self.assertEqual(set(payload["categories"].keys()), set(fetch_news.CATEGORIES))
        self.assertEqual(payload["categories"]["technology"], [{"title": "technology"}])
```

Note: only `fetch_news.datetime` is patched — `timezone` stays the real stdlib object. `build_payload` calls `datetime.now(timezone.utc)`, so the mock receives `timezone.utc` as an argument it ignores; `mock_datetime.now.return_value.date.return_value` is what actually determines the result. No need to touch `timezone` in the mock at all.

Also add to `scripts/test_fetch_news.py` — these drive the exception-handling branch in `main()` with the exact exception types the spec calls out (network error, timeout, malformed JSON), not just a generic `RuntimeError`:

```python
class TestMain(unittest.TestCase):
    def test_missing_api_key_returns_1_without_writing_file(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch("fetch_news.build_payload") as mock_build:
                exit_code = fetch_news.main()
        self.assertEqual(exit_code, 1)
        mock_build.assert_not_called()

    @patch("fetch_news.build_payload")
    def test_build_failure_returns_1_without_writing_file(self, mock_build):
        mock_build.side_effect = RuntimeError("boom")
        with patch.dict(os.environ, {"NEWS_API_KEY": "fake-key"}):
            with patch("fetch_news.OUTPUT_PATH", os.path.join(tempfile.mkdtemp(), "out.json")):
                exit_code = fetch_news.main()
        self.assertEqual(exit_code, 1)

    @patch("fetch_news.build_payload")
    def test_url_error_returns_1(self, mock_build):
        mock_build.side_effect = urllib.error.URLError("network unreachable")
        with patch.dict(os.environ, {"NEWS_API_KEY": "fake-key"}):
            with patch("fetch_news.OUTPUT_PATH", os.path.join(tempfile.mkdtemp(), "out.json")):
                exit_code = fetch_news.main()
        self.assertEqual(exit_code, 1)

    @patch("fetch_news.build_payload")
    def test_timeout_returns_1(self, mock_build):
        mock_build.side_effect = TimeoutError("timed out")
        with patch.dict(os.environ, {"NEWS_API_KEY": "fake-key"}):
            with patch("fetch_news.OUTPUT_PATH", os.path.join(tempfile.mkdtemp(), "out.json")):
                exit_code = fetch_news.main()
        self.assertEqual(exit_code, 1)

    @patch("fetch_news.build_payload")
    def test_malformed_json_returns_1(self, mock_build):
        mock_build.side_effect = json.JSONDecodeError("bad json", "doc", 0)
        with patch.dict(os.environ, {"NEWS_API_KEY": "fake-key"}):
            with patch("fetch_news.OUTPUT_PATH", os.path.join(tempfile.mkdtemp(), "out.json")):
                exit_code = fetch_news.main()
        self.assertEqual(exit_code, 1)

    @patch("fetch_news.build_payload")
    def test_success_writes_file_and_returns_0(self, mock_build):
        mock_build.return_value = {"updated": "2026-01-15", "categories": {}}
        tmp_path = os.path.join(tempfile.mkdtemp(), "out.json")
        with patch.dict(os.environ, {"NEWS_API_KEY": "fake-key"}):
            with patch("fetch_news.OUTPUT_PATH", tmp_path):
                exit_code = fetch_news.main()
        self.assertEqual(exit_code, 0)
        with open(tmp_path) as f:
            written = json.load(f)
        self.assertEqual(written["updated"], "2026-01-15")
```

Add `import urllib.error` to the top of `scripts/test_fetch_news.py` if not already present (needed for `test_url_error_returns_1`).

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest scripts.test_fetch_news -v`
Expected: FAIL — `AttributeError: module 'fetch_news' has no attribute 'build_payload'` (and `main`)

- [ ] **Step 3: Write minimal implementation**

Add to `scripts/fetch_news.py` (after `fetch_category`):

```python
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
```

Note: move the existing `if __name__ == "__main__": unittest.main()` block that lives in `scripts/test_fetch_news.py` — make sure `scripts/fetch_news.py`'s own `if __name__ == "__main__":` block (calling `main()`, not `unittest.main()`) is the last thing in that file, and the test file keeps its own separate `unittest.main()` guard.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest scripts.test_fetch_news -v`
Expected: PASS (16 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch_news.py scripts/test_fetch_news.py
git commit -m "Add build_payload and main with fail-loud error handling"
```

---

### Task 5: GitHub Actions workflow

**Files:**
- Create: `.github/workflows/daily-news.yml`

- [ ] **Step 1: Write the workflow file**

```yaml
name: Daily News

on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch: {}

concurrency:
  group: daily-news
  cancel-in-progress: false

permissions:
  contents: write

jobs:
  fetch-and-commit:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Run unit tests
        run: python3 -m unittest scripts.test_fetch_news -v

      - name: Fetch news
        env:
          NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}
        run: python3 scripts/fetch_news.py

      - name: Commit and push if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git pull --rebase
          git add data/daily-news.json
          git diff --cached --quiet || git commit -m "Update daily news"
          git push
```

Only official GitHub-owned actions are used (`actions/checkout`, `actions/setup-python`) — no third-party commit action, keeping the supply-chain surface minimal per the design doc.

- [ ] **Step 2: Validate YAML syntax locally**

Run: `python3 -c "import yaml, sys; yaml.safe_load(open('.github/workflows/daily-news.yml'))" 2>/dev/null || python3 -c "import json,sys; import subprocess; print('no local yaml validator, will validate on push')"`

If `pyyaml` isn't installed, skip local validation — GitHub validates the workflow file automatically when it's pushed, and any syntax error surfaces immediately in the Actions tab.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/daily-news.yml
git commit -m "Add daily news GitHub Actions workflow"
```

---

### Task 6: End-to-end verification (requires pushing to GitHub — confirm with user first)

**Files:** none (verification only)

- [ ] **Step 1: Confirm with the user before pushing**

This is the first step in this plan that touches the shared remote repository. Ask the user for explicit go-ahead before running `git push`, per the standing rule on actions with blast radius beyond the local machine.

- [ ] **Step 2: Push to `main`**

```bash
git push
```

- [ ] **Step 3: Manually trigger the workflow**

In the GitHub UI: repo → **Actions** tab → **Daily News** workflow → **Run workflow** button (this is what `workflow_dispatch` enables).

- [ ] **Step 4: Verify the run**

Check in the Actions tab:
- The run shows the "Run unit tests" step passing (16 tests).
- The "Fetch news" step completes without error.
- The "Commit and push if changed" step either commits (if data changed) or no-ops cleanly (if content was identical — unlikely on first run).

Then check the repo: `data/daily-news.json` should have a fresh `updated` date and a commit authored by `github-actions[bot]`.

- [ ] **Step 5: Spot-check the rendered site**

Visit `https://www.firatselcuk.dev/news.html` (may take a few minutes for the `raw.githubusercontent.com` CDN cache to clear) and confirm the three category sections show current articles.
