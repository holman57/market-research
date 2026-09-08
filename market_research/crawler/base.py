"""
Base crawler abstractions for Market Research signal ingestion.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
from market_research.models import RawSignal


@dataclass
class CrawlResult:
    """Outcome of a crawl execution."""
    success: bool
    source_name: str
    query: Optional[str]
    signals: List[RawSignal] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.signals)


class BaseCrawler(ABC):
    """Abstract interface for all data source crawlers."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def crawl(self, query: Optional[str] = None, limit: int = 50) -> CrawlResult:
        """Collect raw market signals matching an optional search query."""
        pass
