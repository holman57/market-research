"""
Content brief generator translating market research into production-ready assets.
"""

from __future__ import annotations
from typing import List
from market_research.models import ContentBrief, NicheOpportunity


class ContentGenerator:
    """Generates structured content briefs, hooks, and production outlines."""

    def generate_brief(self, niche: NicheOpportunity) -> ContentBrief:
        """Transforms a niche opportunity into a concrete content outline and brief."""
        primary_kw = niche.keywords[0] if niche.keywords else niche.title.lower()
        secondary_kws = niche.keywords[1:5] if len(niche.keywords) > 1 else []

        title = f"The Definitive Guide to {niche.title}: Fixing Common Pitfalls in 2026"
        hook = (
            f"If you are struggling with {primary_kw}, you are not alone. Across Reddit and "
            f"industry forums, hundreds of practitioners are hitting the same bottleneck. "
            f"Here is how to solve it systematically."
        )

        outline = [
            f"1. Executive Summary: What is {primary_kw} and Why is it Trending Now?",
            f"2. The Core Problem: Why Current Tools and Frameworks Fall Short",
            f"3. Practical Blueprint: Step-by-Step Implementation and Configuration",
            f"4. Cost & Performance Benchmark: Real-World Comparisons",
            f"5. Common Traps & Antipatterns to Avoid",
            f"6. Final Checklist and Recommended Next Steps",
        ]

        pain_points = [
            f"Complexity in initial setup and maintenance",
            f"Unclear error messages and lack of production-grade documentation",
            f"High hidden costs of commercial proprietary alternatives",
        ]

        return ContentBrief(
            title=title,
            target_keyword=primary_kw,
            secondary_keywords=secondary_kws,
            target_audience=niche.target_audience,
            hook=hook,
            outline_sections=outline,
            pain_points_addressed=pain_points,
            recommended_format="Deep Dive Guide",
        )

    def generate_briefs_for_niches(self, niches: List[NicheOpportunity]) -> List[ContentBrief]:
        """Generate a collection of content briefs for top niches."""
        return [self.generate_brief(n) for n in niches]
