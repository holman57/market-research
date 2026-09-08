"""
Niche discovery engine for identifying underserved, high-potential content topics.
"""

from __future__ import annotations
import re
from typing import List

from market_research.models import NicheOpportunity, TopicCluster, TopicScore


class NicheFinder:
    """Filters, refines, and highlights high-leverage content niches from scored topics."""

    def identify_niches(
        self,
        clusters: List[TopicCluster],
        scores: List[TopicScore],
        min_opportunity: float = 50.0,
        limit: int = 10,
    ) -> List[NicheOpportunity]:
        """
        Synthesizes topic clusters and scores into actionable content niche opportunities.
        """
        score_map = {s.topic_name.lower(): s for s in scores}
        niches: List[NicheOpportunity] = []

        for cluster in clusters:
            score = score_map.get(cluster.name.lower())
            if not score or score.opportunity_score < min_opportunity:
                continue

            # Determine competition level
            if score.saturation_score < 40.0:
                comp_level = "Low"
            elif score.saturation_score < 70.0:
                comp_level = "Medium"
            else:
                comp_level = "High"

            # Determine content gap description
            if cluster.pain_density > 0.4:
                gap = f"Audience reports severe friction and missing solutions around {cluster.name.lower()}."
            elif score.velocity_score > 60.0 and comp_level == "Low":
                gap = f"Fast-growing discussion surge with minimal authoritative content published."
            else:
                gap = f"Opportunity for comprehensive comparison and tactical walkthroughs."

            # Generate targeted angles
            angles = [
                f"The No-Nonsense Guide to {cluster.name}: Architecture, Setup, and Gotchas",
                f"Why Most Solutions for {cluster.name} Fail (And How to Fix It)",
                f"{cluster.name} vs Traditional Alternatives: An Honest Benchmark",
                f"How to Automate {cluster.name} on a Budget",
            ]

            niche_id = f"niche_{re.sub(r'[^a-zA-Z0-9]', '_', cluster.name.lower())}"

            niches.append(
                NicheOpportunity(
                    niche_id=niche_id,
                    title=f"{cluster.name} Solutions & Implementation",
                    category="Technology & Strategy",
                    target_audience="Engineers, Technical Founders & Content Creators",
                    opportunity_score=score.opportunity_score,
                    competition_level=comp_level,
                    content_gap=gap,
                    suggested_angles=angles,
                    core_questions=cluster.questions,
                    keywords=cluster.keywords[:6],
                )
            )

        # Sort by opportunity score descending
        niches.sort(key=lambda n: n.opportunity_score, reverse=True)
        return niches[:limit]
