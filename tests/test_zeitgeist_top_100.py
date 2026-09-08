"""
Unit tests for the Cultural Zeitgeist Top 100 module.
"""

from __future__ import annotations
import json
import unittest
from unittest.mock import MagicMock, patch

from market_research.inquiry.zeitgeist_top_100 import (
    ZEITGEIST_DOMAINS,
    generate_top_100_split_reports,
    post_top_100_zeitgeist_issue,
)
from market_research.cli import main as cli_main


class TestZeitgeistTop100(unittest.TestCase):

    def test_domains_and_topic_count(self):
        """Verify exactly 10 domains, 10 topics each, totaling 100 unique topics."""
        self.assertEqual(len(ZEITGEIST_DOMAINS), 10, "Should have exactly 10 cultural domains")

        total_topics = 0
        seen_ids = set()
        seen_titles = set()

        for domain in ZEITGEIST_DOMAINS:
            self.assertIn("domain", domain)
            self.assertIn("icon", domain)
            self.assertIn("topics", domain)
            topics = domain["topics"]
            self.assertEqual(len(topics), 10, f"Domain '{domain['domain']}' must have exactly 10 topics")

            for topic in topics:
                total_topics += 1
                topic_id = topic["id"]
                topic_title = topic["title"]

                # Ensure uniqueness
                self.assertNotIn(topic_id, seen_ids, f"Duplicate topic ID: {topic_id}")
                self.assertNotIn(topic_title, seen_titles, f"Duplicate topic title: {topic_title}")
                seen_ids.add(topic_id)
                seen_titles.add(topic_title)

                # Ensure non-empty required fields
                self.assertTrue(bool(topic.get("hook")), f"Topic {topic_id} missing hook")
                self.assertTrue(bool(topic.get("discussions")), f"Topic {topic_id} missing discussions")
                self.assertTrue(bool(topic.get("artifacts")), f"Topic {topic_id} missing artifacts")
                self.assertTrue(bool(topic.get("angle")), f"Topic {topic_id} missing angle")
                self.assertTrue(0 <= topic.get("velocity", 0) <= 100, f"Topic {topic_id} velocity out of range")
                self.assertTrue(0 <= topic.get("engagement", 0) <= 100, f"Topic {topic_id} engagement out of range")

        self.assertEqual(total_topics, 100, "Total topics across all domains must equal 100")
        self.assertEqual(seen_ids, set(range(1, 101)), "Topic IDs must be contiguous 1 through 100")

    def test_generate_top_100_split_reports(self):
        """Verify split reports fit within GitHub limits and contain correct slices."""
        part1, part2 = generate_top_100_split_reports()

        # Check byte size limits (< 65536 bytes)
        part1_bytes = len(part1.encode("utf-8"))
        part2_bytes = len(part2.encode("utf-8"))

        self.assertLess(part1_bytes, 65000, f"Part 1 exceeds safe GitHub size: {part1_bytes} bytes")
        self.assertLess(part2_bytes, 65000, f"Part 2 exceeds safe GitHub size: {part2_bytes} bytes")

        # Check headers & contents
        self.assertIn("The Cultural Zeitgeist 100", part1)
        self.assertIn("Master Directory Table", part1)
        self.assertIn("The Dumbphone Migration", part1)
        self.assertIn("#### #50. Hyper-Niche Wikipedia Deep-Sea Diving", part1)

        # Check part 2
        self.assertIn("Part 2: Detailed Cultural Breakdown", part2)
        self.assertIn("#### #51. Blueprint Longevity & Epigenetic Clock Tracking", part2)
        self.assertIn("#### #100. Community Tool Libraries & Shared Workshops", part2)
        self.assertIn("Tactical Synthesis for Creators & Content Engines", part2)

    @patch("subprocess.run")
    def test_post_top_100_issue_create(self, mock_run):
        """Test creating a new top 100 issue via gh CLI."""
        # Call 1: gh issue list returns empty
        mock_list = MagicMock()
        mock_list.stdout = "[]"
        mock_list.returncode = 0

        # Call 2: gh issue create returns issue URL
        mock_create = MagicMock()
        mock_create.stdout = "https://github.com/holman57/market-research/issues/4\n"
        mock_create.returncode = 0

        # Call 3: gh issue comment returns comment URL
        mock_comment = MagicMock()
        mock_comment.stdout = "https://github.com/holman57/market-research/issues/4#issuecomment-101\n"
        mock_comment.returncode = 0

        mock_run.side_effect = [mock_list, mock_create, mock_comment]

        res = post_top_100_zeitgeist_issue(repo="holman57/market-research", assignee="holman57")
        self.assertEqual(res["action"], "created")
        self.assertEqual(res["issue_number"], 4)
        self.assertEqual(res["issue_url"], "https://github.com/holman57/market-research/issues/4")

        # Verify arguments used --body-file instead of --body
        create_args = mock_run.call_args_list[1][0][0]
        self.assertIn("--body-file", create_args)
        comment_args = mock_run.call_args_list[2][0][0]
        self.assertIn("--body-file", comment_args)

    @patch("subprocess.run")
    def test_post_top_100_issue_update(self, mock_run):
        """Test updating an existing top 100 issue via gh CLI."""
        # Call 1: gh issue list returns existing issue
        mock_list = MagicMock()
        mock_list.stdout = json.dumps([{
            "number": 4,
            "title": "[Cultural Zeitgeist] Top 100 Niche Topics & Subcultures in the Cultural Zeitgeist (2026 Edition)",
            "url": "https://github.com/holman57/market-research/issues/4"
        }])
        mock_list.returncode = 0

        # Call 2: gh issue edit
        mock_edit = MagicMock()
        mock_edit.stdout = ""
        mock_edit.returncode = 0

        # Call 3: gh issue comment
        mock_comment = MagicMock()
        mock_comment.stdout = "https://github.com/holman57/market-research/issues/4#issuecomment-102\n"
        mock_comment.returncode = 0

        mock_run.side_effect = [mock_list, mock_edit, mock_comment]

        res = post_top_100_zeitgeist_issue(repo="holman57/market-research", assignee="holman57")
        self.assertEqual(res["action"], "updated")
        self.assertEqual(res["issue_number"], 4)

        # Verify arguments used --body-file
        edit_args = mock_run.call_args_list[1][0][0]
        self.assertIn("--body-file", edit_args)
        comment_args = mock_run.call_args_list[2][0][0]
        self.assertIn("--body-file", comment_args)

    @patch("market_research.inquiry.zeitgeist_top_100.post_top_100_zeitgeist_issue")
    def test_cli_zeitgeist_100_post(self, mock_post):
        """Test the CLI subcommand `zeitgeist-100 --post`."""
        mock_post.return_value = {
            "action": "created",
            "repo": "holman57/market-research",
            "issue_number": 4,
            "issue_url": "https://github.com/holman57/market-research/issues/4"
        }

        ret = cli_main(["zeitgeist-100", "--post", "--repo", "holman57/market-research"])
        self.assertEqual(ret, 0)
        mock_post.assert_called_once_with(repo="holman57/market-research", assignee="holman57")


if __name__ == "__main__":
    unittest.main()
