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
