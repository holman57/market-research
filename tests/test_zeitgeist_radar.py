"""
Unit tests for the Zeitgeist Radar cultural intelligence synthesizer.
"""

from __future__ import annotations
import unittest
from unittest.mock import MagicMock, patch

from market_research.inquiry.zeitgeist_radar import ZeitgeistRadar, ZeitgeistRadarReport


class TestZeitgeistRadar(unittest.TestCase):

    def setUp(self):
        self.radar = ZeitgeistRadar()

    def test_generate_report_structure(self):
        report = self.radar.generate_report()
        self.assertIsInstance(report, ZeitgeistRadarReport)
        self.assertTrue(len(report.topics_by_pillar) >= 4)

        # Check all 4 core pillars requested by user
        self.assertIn("Subcultures & Online Tribes", report.topics_by_pillar)
        self.assertIn("Anti-Trends & Counter-Movements", report.topics_by_pillar)
        self.assertIn("Micro-Aesthetics & Sensibilities", report.topics_by_pillar)
        self.assertIn("Social Shifts & Behavioral Realignments", report.topics_by_pillar)

        # Verify items inside pillars
        for pillar, topics in report.topics_by_pillar.items():
            self.assertTrue(len(topics) >= 3, f"Pillar {pillar} should have at least 3 topics")
            for t in topics:
                self.assertTrue(bool(t.title))
                self.assertTrue(bool(t.hook))
                self.assertTrue(bool(t.breakdown))
                self.assertTrue(len(t.active_discussions) > 0)
                self.assertTrue(len(t.rituals_and_artifacts) > 0)
                self.assertTrue(len(t.content_angles) > 0)

    def test_format_markdown_report(self):
        report = self.radar.generate_report()
        md = self.radar.format_markdown_report(report)

        self.assertIn("# Cultural Zeitgeist Radar", md)
        self.assertIn("Subcultures & Online Tribes", md)
        self.assertIn("Anti-Trends & Counter-Movements", md)
        self.assertIn("Micro-Aesthetics & Sensibilities", md)
        self.assertIn("Social Shifts & Behavioral Realignments", md)
        self.assertIn("What the Internet is Actively Discussing", md)
        self.assertIn("Tangible Artifacts & Participation Rituals", md)
        self.assertIn("Actionable Strategic Takeaways", md)

    @patch("subprocess.run")
    def test_sync_to_github_create_new(self, mock_run):
        # Case 1: No existing issue
        # First call: gh issue list returns empty list
        mock_list_proc = MagicMock()
        mock_list_proc.stdout = "[]"
        mock_list_proc.returncode = 0

        # Second call: gh issue create returns issue URL
        mock_create_proc = MagicMock()
        mock_create_proc.stdout = "https://github.com/holman57/market-research/issues/42\n"
        mock_create_proc.returncode = 0

        mock_run.side_effect = [mock_list_proc, mock_create_proc]

        res = self.radar.sync_to_github(repo="holman57/market-research", assignee="holman57")
        self.assertEqual(res["action"], "created")
        self.assertEqual(res["issue_number"], 42)

    @patch("subprocess.run")
    def test_sync_to_github_update_existing(self, mock_run):
        # Case 2: Existing issue
        mock_list_proc = MagicMock()
        mock_list_proc.stdout = '[{"number": 2, "title": "[Cultural Zeitgeist] Daily Niche Popular Culture & Subculture Radar", "url": "https://github.com/holman57/market-research/issues/2"}]'
        mock_list_proc.returncode = 0

        mock_edit_proc = MagicMock()
        mock_edit_proc.stdout = ""
        mock_edit_proc.returncode = 0

        mock_comment_proc = MagicMock()
        mock_comment_proc.stdout = "https://github.com/holman57/market-research/issues/2#issuecomment-12345\n"
        mock_comment_proc.returncode = 0

        mock_run.side_effect = [mock_list_proc, mock_edit_proc, mock_comment_proc]

        res = self.radar.sync_to_github(repo="holman57/market-research", assignee="holman57")
        self.assertEqual(res["action"], "updated")
        self.assertEqual(res["issue_number"], 2)


if __name__ == "__main__":
    unittest.main()
