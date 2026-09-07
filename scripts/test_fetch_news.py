import json
import os
import sys
import tempfile
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

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

    @patch("fetch_news.urllib.request.urlopen")
    def test_sends_correct_request_shape(self, mock_urlopen):
        body = {
            "status": "ok",
            "articles": [
                {
                    "title": "Real",
                    "description": "d",
                    "url": "https://x.com",
                    "source": {"name": "BBC"},
                    "publishedAt": "p",
                    "urlToImage": "i",
                }
            ],
        }
        mock_urlopen.return_value = self._mock_response(body)

        fetch_news.fetch_category("technology", "fake-key")

        args, _ = mock_urlopen.call_args
        request = args[0]
        self.assertIn("category=technology", request.full_url)
        self.assertIn("pageSize=5", request.full_url)
        self.assertIn("country=us", request.full_url)
        self.assertEqual(request.get_header("X-api-key"), "fake-key")


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
        tmp_path = os.path.join(tempfile.mkdtemp(), "out.json")
        with patch.dict(os.environ, {"NEWS_API_KEY": "fake-key"}):
            with patch("fetch_news.OUTPUT_PATH", tmp_path):
                exit_code = fetch_news.main()
        self.assertEqual(exit_code, 1)
        self.assertFalse(os.path.exists(tmp_path))

    @patch("fetch_news.build_payload")
    def test_url_error_returns_1(self, mock_build):
        mock_build.side_effect = urllib.error.URLError("network unreachable")
        tmp_path = os.path.join(tempfile.mkdtemp(), "out.json")
        with patch.dict(os.environ, {"NEWS_API_KEY": "fake-key"}):
            with patch("fetch_news.OUTPUT_PATH", tmp_path):
                exit_code = fetch_news.main()
        self.assertEqual(exit_code, 1)
        self.assertFalse(os.path.exists(tmp_path))

    @patch("fetch_news.build_payload")
    def test_timeout_returns_1(self, mock_build):
        mock_build.side_effect = TimeoutError("timed out")
        tmp_path = os.path.join(tempfile.mkdtemp(), "out.json")
        with patch.dict(os.environ, {"NEWS_API_KEY": "fake-key"}):
            with patch("fetch_news.OUTPUT_PATH", tmp_path):
                exit_code = fetch_news.main()
        self.assertEqual(exit_code, 1)
        self.assertFalse(os.path.exists(tmp_path))

    @patch("fetch_news.build_payload")
    def test_malformed_json_returns_1(self, mock_build):
        mock_build.side_effect = json.JSONDecodeError("bad json", "doc", 0)
        tmp_path = os.path.join(tempfile.mkdtemp(), "out.json")
        with patch.dict(os.environ, {"NEWS_API_KEY": "fake-key"}):
            with patch("fetch_news.OUTPUT_PATH", tmp_path):
                exit_code = fetch_news.main()
        self.assertEqual(exit_code, 1)
        self.assertFalse(os.path.exists(tmp_path))

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


if __name__ == "__main__":
    unittest.main()
