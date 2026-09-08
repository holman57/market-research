"""
Tests for niche opportunity discovery and content brief generation.
"""

import unittest
from market_research.analysis.nlp import TopicExtractor
from market_research.crawler.web_crawler import WebCrawler
from market_research.discovery.content_generator import ContentGenerator
from market_research.discovery.niche_finder import NicheFinder
from market_research.scoring.scorer import TopicScorer


class TestNicheFinder(unittest.TestCase):

    def setUp(self):
        self.crawler = WebCrawler()
        self.extractor = TopicExtractor()
        self.scorer = TopicScorer()
        self.niche_finder = NicheFinder()
        self.content_generator = ContentGenerator()

    def test_identify_niches_and_generate_briefs(self):
        signals = self.crawler.generate_synthetic_signals("Decentralized Storage", count=12)
        clusters = self.extractor.cluster_signals(signals)
        scores = self.scorer.score_all(clusters)

        niches = self.niche_finder.identify_niches(clusters, scores, min_opportunity=10.0, limit=5)
        self.assertGreater(len(niches), 0)

        top_niche = niches[0]
        self.assertTrue(top_niche.niche_id.startswith("niche_"))
        self.assertIn(top_niche.competition_level, ["Low", "Medium", "High"])
        self.assertGreater(len(top_niche.suggested_angles), 0)

        # Content brief generation
        brief = self.content_generator.generate_brief(top_niche)
        self.assertIn("Guide", brief.title)
        self.assertTrue(len(brief.hook) > 20)
        self.assertGreater(len(brief.outline_sections), 3)
        self.assertGreater(len(brief.pain_points_addressed), 0)


if __name__ == "__main__":
    unittest.main()
