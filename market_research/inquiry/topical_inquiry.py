"""
End-to-end topical inquiry engine orchestrating crawling, analysis, scoring, and brief generation.
"""

from __future__ import annotations
from datetime import datetime, timezone
import json
from typing import Optional

from market_research.analysis.nlp import TopicExtractor
from market_research.config import Config
from market_research.crawler.web_crawler import WebCrawler
from market_research.discovery.content_generator import ContentGenerator
from market_research.discovery.niche_finder import NicheFinder
from market_research.models import InquiryDossier
from market_research.scoring.scorer import TopicScorer


class TopicalInquiryEngine:
    """Orchestrates comprehensive market research and topical inquiry workflows."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.default()
        self.crawler = WebCrawler(self.config.crawler)
        self.extractor = TopicExtractor()
        self.scorer = TopicScorer(self.config.scoring)
        self.niche_finder = NicheFinder()
        self.content_generator = ContentGenerator()

    def run_inquiry(self, subject: str, limit: int = 25) -> InquiryDossier:
        """
        Executes a complete topical inquiry pipeline for a given subject.
        """
        # 1. Crawl raw signals
        crawl_result = self.crawler.crawl(query=subject, limit=limit)
        signals = crawl_result.signals

        # 2. Extract clusters and themes
        clusters = self.extractor.cluster_signals(signals)

        # 3. Score topics
        scores = self.scorer.score_all(clusters)

        # 4. Discover niches
        niches = self.niche_finder.identify_niches(
            clusters=clusters,
            scores=scores,
            min_opportunity=self.config.discovery.min_opportunity_score,
            limit=self.config.discovery.max_niches_per_report,
        )

        # 5. Generate content briefs
        briefs = self.content_generator.generate_briefs_for_niches(niches[:3])

        # 6. Aggregate questions
        all_questions = []
        for c in clusters:
            all_questions.extend(c.questions)
        unique_questions = list(dict.fromkeys(all_questions))[:8]

        summary = (
            f"Topical inquiry into '{subject}' analyzed {len(signals)} signals across community "
            f"discussions, search trends, and forum queries. Identified {len(clusters)} core topic clusters "
            f"and {len(niches)} high-opportunity content niches with strong market appetite."
        )

        return InquiryDossier(
            subject=subject,
            generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            executive_summary=summary,
            total_signals_analyzed=len(signals),
            top_topics=scores[:5],
            top_niches=niches,
            content_briefs=briefs,
            common_questions=unique_questions,
        )

    def export_markdown(self, dossier: InquiryDossier) -> str:
        """Render the inquiry dossier as an actionable markdown report."""
        lines = [
            f"# Market Research Dossier: {dossier.subject}",
            f"**Generated:** {dossier.generated_at} | **Signals Analyzed:** {dossier.total_signals_analyzed}",
            "",
            "## Executive Summary",
            dossier.executive_summary,
            "",
            "## Top Scored Topics",
            "| Topic | Velocity | Engagement | Saturation | Monetization | Opportunity |",
            "| :--- | :---: | :---: | :---: | :---: | :---: |",
        ]

        for t in dossier.top_topics:
            lines.append(
                f"| **{t.topic_name}** | {t.velocity_score} | {t.engagement_score} | "
                f"{t.saturation_score} | {t.monetization_score} | **{t.opportunity_score}** |"
            )

        lines.extend([
            "",
            "## High-Leverage Niche Opportunities",
        ])

        for n in dossier.top_niches:
            lines.extend([
                f"### {n.title} (Score: {n.opportunity_score}/100, Competition: {n.competition_level})",
                f"- **Target Audience:** {n.target_audience}",
                f"- **Content Gap:** {n.content_gap}",
                f"- **Keywords:** {', '.join(n.keywords)}",
                "- **Suggested Content Angles:**",
            ])
            for angle in n.suggested_angles:
                lines.append(f"  - {angle}")
            lines.append("")

        if dossier.common_questions:
            lines.extend([
                "## Frequent Community Questions",
            ])
            for q in dossier.common_questions:
                lines.append(f"- {q}")
            lines.append("")

        if dossier.content_briefs:
            lines.extend([
                "## Production-Ready Content Briefs",
            ])
            for idx, b in enumerate(dossier.content_briefs, 1):
                lines.extend([
                    f"### Brief #{idx}: {b.title}",
                    f"- **Format:** {b.recommended_format}",
                    f"- **Target Keyword:** `{b.target_keyword}`",
                    f'- **Hook:** *"{b.hook}"*',
                    "- **Outline Blueprint:**",
                ])
                for item in b.outline_sections:
                    lines.append(f"  - {item}")
                lines.append("")

        return "\n".join(lines)
