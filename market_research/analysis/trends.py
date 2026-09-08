"""
Trend velocity and temporal momentum analysis for market signals.
"""

from __future__ import annotations
import time
from typing import List
from market_research.models import RawSignal


class TrendAnalyzer:
    """Computes discussion velocity, temporal momentum, and growth trends."""

    def calculate_velocity(self, signals: List[RawSignal], window_hours: float = 48.0) -> float:
        """
        Calculates signal velocity (signals per hour normalized to a 0-100 score).
        """
        if not signals:
            return 0.0

        now = time.time()
        cutoff = now - (window_hours * 3600)
        recent_signals = [s for s in signals if s.timestamp >= cutoff]

        rate_per_day = (len(recent_signals) / max(1.0, window_hours)) * 24.0

        # Normalization: 20+ signals/day represents peak 100 velocity
        velocity_score = min(100.0, (rate_per_day / 20.0) * 100.0)
        return round(velocity_score, 2)

    def calculate_engagement_resonance(self, signals: List[RawSignal]) -> float:
        """
        Measures audience resonance based on comment-to-upvote depth and interaction.
        """
        if not signals:
            return 0.0

        total_upvotes = sum(s.upvotes for s in signals)
        total_comments = sum(s.comments_count for s in signals)

        avg_upvotes = total_upvotes / len(signals)
        avg_comments = total_comments / len(signals)

        # Discussion depth score: higher comments per upvote signifies intense conversation
        interaction_intensity = (avg_upvotes * 0.4) + (avg_comments * 1.5)
        score = min(100.0, interaction_intensity / 2.5)
        return round(score, 2)
