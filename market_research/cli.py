"""
Command-line interface for the Market Research engine.
"""

from __future__ import annotations
import argparse
import json
import sys
from typing import List, Optional

from market_research.crawler.web_crawler import WebCrawler
from market_research.analysis.nlp import TopicExtractor
from market_research.config import Config
from market_research.discovery.niche_finder import NicheFinder
from market_research.inquiry.topical_inquiry import TopicalInquiryEngine
from market_research.inquiry.zeitgeist_radar import ZeitgeistRadar
from market_research.scoring.scorer import TopicScorer


def cmd_inquire(args: argparse.Namespace) -> int:
    """Run an end-to-end topical inquiry."""
    print(f"[*] Starting topical inquiry for: '{args.subject}' (limit: {args.limit} signals)...")
    engine = TopicalInquiryEngine()
    dossier = engine.run_inquiry(args.subject, limit=args.limit)

    markdown_report = engine.export_markdown(dossier)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            if args.output.endswith(".json"):
                data = {
                    "subject": dossier.subject,
                    "generated_at": dossier.generated_at,
                    "executive_summary": dossier.executive_summary,
                    "total_signals_analyzed": dossier.total_signals_analyzed,
                    "top_topics": [t.__dict__ for t in dossier.top_topics],
                    "top_niches": [n.__dict__ for n in dossier.top_niches],
                    "content_briefs": [b.__dict__ for b in dossier.content_briefs],
                    "common_questions": dossier.common_questions,
                }
                json.dump(data, f, indent=2)
            else:
                f.write(markdown_report)
        print(f"[+] Dossier successfully saved to: {args.output}")
    else:
        print()
        print(markdown_report)

    return 0


def cmd_crawl(args: argparse.Namespace) -> int:
    """Crawl web sources for topic signals."""
    print(f"[*] Crawling signals for query: '{args.query}' (limit: {args.limit})...")
    crawler = WebCrawler()
    result = crawler.crawl(query=args.query, limit=args.limit)

    print(f"[+] Successfully harvested {result.count} signals.")
    for idx, sig in enumerate(result.signals[:5], 1):
        print(f"  {idx}. [{sig.source.value.upper()}] {sig.title} (Upvotes: {sig.upvotes}, Comments: {sig.comments_count})")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            signals_data = [s.__dict__ for s in result.signals]
            for s in signals_data:
                s["source"] = str(s["source"])
            json.dump(signals_data, f, indent=2)
        print(f"[+] Dumped raw signals to {args.output}")

    return 0


def cmd_score(args: argparse.Namespace) -> int:
    """Score conversation topics."""
    query = args.query or "trending"
    print(f"[*] Scoring active topics for: '{query}'...")
    crawler = WebCrawler()
    extractor = TopicExtractor()
    scorer = TopicScorer()

    signals = crawler.crawl(query=query, limit=args.limit).signals
    clusters = extractor.cluster_signals(signals)
    scores = scorer.score_all(clusters)

    print()
    print("--- Topic Scores ---")
    print(f"{'Topic':<25} {'Velocity':<10} {'Engage':<10} {'Saturation':<12} {'Opportunity':<12}")
    print("-" * 72)
    for s in scores:
        print(f"{s.topic_name:<25} {s.velocity_score:<10.1f} {s.engagement_score:<10.1f} {s.saturation_score:<12.1f} {s.opportunity_score:<12.1f}")

    return 0


def cmd_discover(args: argparse.Namespace) -> int:
    """Discover unsaturated content niches."""
    query = args.query or "software development"
    print(f"[*] Discovering niche opportunities for: '{query}'...")
    crawler = WebCrawler()
    extractor = TopicExtractor()
    scorer = TopicScorer()
    finder = NicheFinder()

    signals = crawler.crawl(query=query, limit=args.limit).signals
    clusters = extractor.cluster_signals(signals)
    scores = scorer.score_all(clusters)
    niches = finder.identify_niches(clusters, scores, min_opportunity=args.min_score)

    print()
    print(f"[+] Found {len(niches)} high-opportunity niches:")
    for n in niches:
        print()
        print(f"-> {n.title} (Opportunity: {n.opportunity_score}/100, Comp: {n.competition_level})")
        print(f"   Gap: {n.content_gap}")
        print(f"   Angles: {n.suggested_angles[0] if n.suggested_angles else 'N/A'}")

    return 0


def cmd_zeitgeist(args: argparse.Namespace) -> int:
    """Generate or sync the daily Cultural Zeitgeist Radar."""
    radar = ZeitgeistRadar()
    if args.sync:
        print(f"[*] Synchronizing Cultural Zeitgeist Radar to GitHub ({args.repo})...")
        res = radar.sync_to_github(repo=args.repo, assignee=args.assignee)
        print(f"[+] Result: {res}")
        return 0

    report = radar.generate_report()
    md = radar.format_markdown_report(report)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"[+] Saved report to: {args.output}")
    else:
        print(md)
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Construct CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="market-research",
        description="Market Research: Web Crawler & Topic Scoring for Content Generation and Topical Inquiry.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Inquire subcommand
    inquire_parser = subparsers.add_parser("inquire", help="Run full topical inquiry and generate research dossier")
    inquire_parser.add_argument("subject", type=str, help="Subject or seed topic to research")
    inquire_parser.add_argument("--limit", type=int, default=25, help="Number of signals to harvest (default: 25)")
    inquire_parser.add_argument("-o", "--output", type=str, default=None, help="Output file path (.md or .json)")

    # Crawl subcommand
    crawl_parser = subparsers.add_parser("crawl", help="Harvest raw discussion signals from web sources")
    crawl_parser.add_argument("--query", type=str, default="trending", help="Query or keyword to target")
    crawl_parser.add_argument("--limit", type=int, default=25, help="Signal count limit")
    crawl_parser.add_argument("-o", "--output", type=str, default=None, help="Output JSON path")

    # Score subcommand
    score_parser = subparsers.add_parser("score", help="Score topics extracted from signals")
    score_parser.add_argument("--query", type=str, default="technology", help="Target query")
    score_parser.add_argument("--limit", type=int, default=25, help="Signal count limit")

    # Discover subcommand
    discover_parser = subparsers.add_parser("discover", help="Discover unsaturated content niches")
    discover_parser.add_argument("--query", type=str, default="developer tools", help="Seed theme")
    discover_parser.add_argument("--limit", type=int, default=30, help="Signal limit")
    discover_parser.add_argument("--min-score", type=float, default=50.0, help="Minimum opportunity score threshold")

    # Zeitgeist subcommand
    zg_parser = subparsers.add_parser("zeitgeist", help="Generate or sync daily cultural zeitgeist radar")
    zg_parser.add_argument("--sync", action="store_true", help="Sync directly to GitHub issue")
    zg_parser.add_argument("--repo", type=str, default="holman57/market-research", help="GitHub repo")
    zg_parser.add_argument("--assignee", type=str, default="holman57", help="Issue assignee")
    zg_parser.add_argument("-o", "--output", type=str, default=None, help="Output markdown file")

    return parser


def main(args: Optional[List[str]] = None) -> int:
    parser = build_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 1

    if parsed_args.command == "inquire":
        return cmd_inquire(parsed_args)
    elif parsed_args.command == "crawl":
        return cmd_crawl(parsed_args)
    elif parsed_args.command == "score":
        return cmd_score(parsed_args)
    elif parsed_args.command == "discover":
        return cmd_discover(parsed_args)
    elif parsed_args.command == "zeitgeist":
        return cmd_zeitgeist(parsed_args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
