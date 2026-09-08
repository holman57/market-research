"""
Tests for signal ingestion and web crawler mechanisms.
"""

import unittest
from market_research.crawler.web_crawler import WebCrawler
from market_research.models import SourceType


class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.crawler = WebCrawler()

    def test_synthetic_signal_generation(self):
        signals = self.crawler.generate_synthetic_signals("Local LLMs", count=8)
        self.assertEqual(len(signals), 8)

        for sig in signals:
            self.assertTrue(sig.id.startswith("synth_"))
            self.assertIn("Local LLMs", sig.title)
            self.assertTrue(len(sig.body) > 20)
            self.assertIsInstance(sig.source, SourceType)
            self.assertGreaterEqual(sig.upvotes, 0)
            self.assertGreaterEqual(sig.comments_count, 0)

    def test_crawler_returns_expected_limit(self):
        result = self.crawler.crawl(query="Kubernetes alternatives", limit=12)
        self.assertTrue(result.success)
        self.assertEqual(result.count, 12)
        self.assertEqual(len(result.signals), 12)


if __name__ == "__main__":
    unittest.main()
