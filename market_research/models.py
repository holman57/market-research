"""
Core data schemas for the Market Research engine.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import time


class SourceType(str, Enum):
    REDDIT = "reddit"
    HACKER_NEWS = "hackernews"
    RSS_FEED = "rss_feed"
    FORUM = "forum"
    SEARCH_TRENDS = "search_trends"
    WEB = "web"


@dataclass
class RawSignal:
    """Represents an ingested web signal (discussion, post, article, or search item)."""
    id: str
    source: SourceType
    url: str
    title: str
    body: str
    timestamp: float = field(default_factory=time.time)
    author: str = ""
    upvotes: int = 0
    comments_count: int = 0
    shares: int = 0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TopicCluster:
    """Represents a clustered group of related signals around a theme or keyword."""
    name: str
    keywords: List[str]
    signals: List[RawSignal] = field(default_factory=list)
    total_mentions: int = 0
    sentiment_score: float = 0.0  # -1.0 (negative) to 1.0 (positive)
    pain_density: float = 0.0     # 0.0 (no pain/complaints) to 1.0 (high frustration/demand for solutions)
    questions: List[str] = field(default_factory=list)


@dataclass
class TopicScore:
    """Multi-factor scoring breakdown for a topic."""
    topic_name: str
    velocity_score: float         # 0.0 - 100.0 (conversation growth and speed)
    engagement_score: float       # 0.0 - 100.0 (depth of discussion, comments, upvotes)
    saturation_score: float       # 0.0 - 100.0 (existing competition and content density)
    monetization_score: float     # 0.0 - 100.0 (buyer intent, commercial keyword signals)
    opportunity_score: float      # 0.0 - 100.0 (composite viability for new content)
    rationale: List[str] = field(default_factory=list)


@dataclass
class NicheOpportunity:
    """An identified high-potential niche with content gap analysis."""
    niche_id: str
    title: str
    category: str
    target_audience: str
    opportunity_score: float
    competition_level: str        # 'Low', 'Medium', 'High'
    content_gap: str
    suggested_angles: List[str] = field(default_factory=list)
    core_questions: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)


@dataclass
class ContentBrief:
    """Actionable content generation blueprint derived from research."""
    title: str
    target_keyword: str
    secondary_keywords: List[str] = field(default_factory=list)
    target_audience: str = ""
    hook: str = ""
    outline_sections: List[str] = field(default_factory=list)
    pain_points_addressed: List[str] = field(default_factory=list)
    recommended_format: str = "Deep Dive Guide"


@dataclass
class InquiryDossier:
    """Comprehensive topical inquiry dossier compiling all research outputs."""
    subject: str
    generated_at: str
    executive_summary: str
    total_signals_analyzed: int
    top_topics: List[TopicScore] = field(default_factory=list)
    top_niches: List[NicheOpportunity] = field(default_factory=list)
    content_briefs: List[ContentBrief] = field(default_factory=list)
    common_questions: List[str] = field(default_factory=list)
