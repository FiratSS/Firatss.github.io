import json
import os
import sys
import unittest
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


if __name__ == "__main__":
    unittest.main()
