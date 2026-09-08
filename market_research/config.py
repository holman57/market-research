"""
Configuration management for Market Research.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import os


@dataclass
class CrawlerConfig:
    user_agent: str = "MarketResearchBot/1.0 (+https://github.com/LukeH/market-research)"
    request_delay_seconds: float = 1.0
    timeout_seconds: int = 15
    max_concurrency: int = 4
    sources: List[str] = field(
        default_factory=lambda: ["reddit", "hackernews", "rss_feed", "forum", "search_trends"]
    )


@dataclass
class ScoringWeights:
    velocity: float = 0.35
    engagement: float = 0.25
    saturation_penalty: float = 0.20
    monetization: float = 0.20


@dataclass
class DiscoveryConfig:
    min_signals_per_topic: int = 2
    max_niches_per_report: int = 10
    min_opportunity_score: float = 30.0


@dataclass
class Config:
    crawler: CrawlerConfig = field(default_factory=CrawlerConfig)
    scoring: ScoringWeights = field(default_factory=ScoringWeights)
    discovery: DiscoveryConfig = field(default_factory=DiscoveryConfig)
    data_dir: str = "./data"
    reports_dir: str = "./reports"
    cache_dir: str = "./cache"

    @classmethod
    def default(cls) -> Config:
        return cls()
