"""
Tests for NLP analysis, clustering, and topic scoring metrics.
"""

import unittest
from market_research.analysis.nlp import TopicExtractor
from market_research.crawler.web_crawler import WebCrawler
from market_research.models import RawSignal, SourceType, TopicCluster
from market_research.scoring.scorer import TopicScorer


class TestScorer(unittest.TestCase):

    def setUp(self):
        self.extractor = TopicExtractor()
        self.scorer = TopicScorer()
        self.crawler = WebCrawler()

    def test_cluster_extraction(self):
        signals = self.crawler.generate_synthetic_signals("Vector Database", count=10)
        clusters = self.extractor.cluster_signals(signals)

        self.assertGreater(len(clusters), 0)
        top_cluster = clusters[0]
        self.assertIsInstance(top_cluster, TopicCluster)
        self.assertGreater(top_cluster.total_mentions, 0)
        self.assertTrue(len(top_cluster.keywords) > 0)

    def test_scoring_boundaries(self):
        signals = self.crawler.generate_synthetic_signals("NextJS Hosting", count=6)
        clusters = self.extractor.cluster_signals(signals)
        scores = self.scorer.score_all(clusters)

        for score in scores:
            self.assertGreaterEqual(score.velocity_score, 0.0)
            self.assertLessEqual(score.velocity_score, 100.0)
            self.assertGreaterEqual(score.engagement_score, 0.0)
            self.assertLessEqual(score.engagement_score, 100.0)
            self.assertGreaterEqual(score.saturation_score, 0.0)
            self.assertLessEqual(score.saturation_score, 100.0)
            self.assertGreaterEqual(score.monetization_score, 0.0)
            self.assertLessEqual(score.monetization_score, 100.0)
            self.assertGreaterEqual(score.opportunity_score, 0.0)
            self.assertLessEqual(score.opportunity_score, 100.0)
            self.assertTrue(len(score.rationale) > 0)

    def test_pain_words_increase_pain_density(self):
        smooth_text = "Everything is great, working smoothly and easy to use."
        pain_text = "I am frustrated with this bug. It is a slow, broken nightmare and costly to fix."

        density_smooth = self.extractor.calculate_pain_density(smooth_text)
        density_pain = self.extractor.calculate_pain_density(pain_text)

        self.assertGreater(density_pain, density_smooth)


if __name__ == "__main__":
    unittest.main()
