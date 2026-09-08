"""
Multi-factor topic scoring algorithm to identify active and profitable conversation trends.
"""

from __future__ import annotations
from typing import List, Optional

from market_research.analysis.nlp import TopicExtractor
from market_research.analysis.trends import TrendAnalyzer
from market_research.config import ScoringWeights
from market_research.models import TopicCluster, TopicScore


class TopicScorer:
    """
    Computes a composite opportunity score for topics based on conversation velocity,
    user engagement, market saturation, and monetization viability.
    """

    def __init__(self, weights: Optional[ScoringWeights] = None):
        self.weights = weights or ScoringWeights()
        self.extractor = TopicExtractor()
        self.trend_analyzer = TrendAnalyzer()

    def score_topic(self, cluster: TopicCluster) -> TopicScore:
        """Score an individual topic cluster across all key dimensions."""
        rationale: List[str] = []

        # 1. Velocity Score: How quickly are discussions growing?
        velocity_score = self.trend_analyzer.calculate_velocity(cluster.signals)
        if velocity_score > 70:
            rationale.append("Surging conversation velocity across recent windows.")
        elif velocity_score > 40:
            rationale.append("Consistent, healthy conversation volume.")
        else:
            rationale.append("Low or sporadic posting frequency.")

        # 2. Engagement Score: Are people actively reading, upvoting, and replying?
        engagement_score = self.trend_analyzer.calculate_engagement_resonance(cluster.signals)
        if engagement_score > 70:
            rationale.append("High engagement depth: discussions feature strong debate and comment depth.")
        elif engagement_score > 40:
            rationale.append("Moderate engagement across social and community channels.")
        else:
            rationale.append("Passive engagement with limited community participation.")

        # 3. Saturation Score: How crowded is this space?
        # Estimated based on signal count and generic keywords
        saturation_score = min(100.0, (cluster.total_mentions * 4.5) + (len(cluster.keywords) * 3.0))
        # Reduce saturation if pain density is high (meaning existing solutions are inadequate)
        adjusted_saturation = max(10.0, saturation_score - (cluster.pain_density * 30.0))
        if adjusted_saturation > 70:
            rationale.append("High market saturation: many incumbents and existing coverage.")
        elif adjusted_saturation > 40:
            rationale.append("Moderate saturation with identifiable topical blindspots.")
        else:
            rationale.append("Low saturation: clear content gap and underserved audience.")

        # 4. Monetization & Buyer Intent Score
        combined_text = " ".join([f"{s.title} {s.body}" for s in cluster.signals])
        buyer_intent_ratio = self.extractor.calculate_buyer_intent(combined_text)
        monetization_score = min(100.0, (buyer_intent_ratio * 100.0) + (cluster.pain_density * 40.0))
        if monetization_score > 65:
            rationale.append("Strong commercial intent: users seeking tools, comparisons, or paid alternatives.")
        else:
            rationale.append("Informational inquiry with developing commercial intent.")

        # 5. Composite Opportunity Score Formula:
        # High velocity + high engagement + good monetization - saturation penalty + pain bonus
        raw_opportunity = (
            (velocity_score * self.weights.velocity)
            + (engagement_score * self.weights.engagement)
            + (monetization_score * self.weights.monetization)
            - (adjusted_saturation * (self.weights.saturation_penalty * 0.5))
            + (cluster.pain_density * 25.0)
        )

        opportunity_score = round(max(0.0, min(100.0, raw_opportunity)), 2)

        return TopicScore(
            topic_name=cluster.name,
            velocity_score=velocity_score,
            engagement_score=engagement_score,
            saturation_score=round(adjusted_saturation, 2),
            monetization_score=round(monetization_score, 2),
            opportunity_score=opportunity_score,
            rationale=rationale,
        )

    def score_all(self, clusters: List[TopicCluster]) -> List[TopicScore]:
        """Score and rank a list of topic clusters by composite opportunity score."""
        scores = [self.score_topic(c) for c in clusters]
        scores.sort(key=lambda s: s.opportunity_score, reverse=True)
        return scores
