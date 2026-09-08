"""
Metrics and evaluation parameters for market viability scoring.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class MetricWeights:
    velocity: float = 0.35
    engagement: float = 0.25
    saturation_penalty: float = 0.20
    monetization: float = 0.20
