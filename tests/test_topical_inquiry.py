"""
Tests for the full TopicalInquiryEngine pipeline.
"""

import unittest
from market_research.inquiry.topical_inquiry import TopicalInquiryEngine
from market_research.models import InquiryDossier


class TestTopicalInquiry(unittest.TestCase):

    def setUp(self):
        self.engine = TopicalInquiryEngine()

    def test_run_inquiry_pipeline(self):
        dossier = self.engine.run_inquiry("AI Agent Workflows", limit=15)
        self.assertIsInstance(dossier, InquiryDossier)
        self.assertEqual(dossier.subject, "AI Agent Workflows")
        self.assertEqual(dossier.total_signals_analyzed, 15)
        self.assertTrue(len(dossier.executive_summary) > 20)
        self.assertGreater(len(dossier.top_topics), 0)

    def test_markdown_export(self):
        dossier = self.engine.run_inquiry("Open Source Analytics", limit=10)
        md = self.engine.export_markdown(dossier)

        self.assertIn("# Market Research Dossier: Open Source Analytics", md)
        self.assertIn("## Executive Summary", md)
        self.assertIn("## Top Scored Topics", md)
        self.assertIn("Velocity", md)


if __name__ == "__main__":
    unittest.main()
