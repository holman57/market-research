"""
Source definitions and feed endpoints for market signal harvesting.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
from market_research.models import SourceType


@dataclass
class SourceDefinition:
    key: str
    source_type: SourceType
    display_name: str
    description: str
    default_enabled: bool = True


DEFAULT_SOURCES: Dict[str, SourceDefinition] = {
    "reddit": SourceDefinition(
        key="reddit",
        source_type=SourceType.REDDIT,
        display_name="Reddit Discussions",
        description="Active community subreddits, problem threads, and product queries.",
    ),
    "hackernews": SourceDefinition(
        key="hackernews",
        source_type=SourceType.HACKER_NEWS,
        display_name="Hacker News",
        description="Tech community submissions, 'Show HN', 'Ask HN', and discussions.",
    ),
    "rss_feed": SourceDefinition(
        key="rss_feed",
        source_type=SourceType.RSS_FEED,
        display_name="Industry RSS & Blogs",
        description="Topical RSS syndications, industry newsletters, and blogs.",
    ),
    "forum": SourceDefinition(
        key="forum",
        source_type=SourceType.FORUM,
        display_name="Specialized Forums",
        description="Niche-specific forums, StackExchange, Discourse communities.",
    ),
    "search_trends": SourceDefinition(
        key="search_trends",
        source_type=SourceType.SEARCH_TRENDS,
        display_name="Search & Trend Signals",
        description="Search volume momentum and 'People Also Ask' question streams.",
    ),
}
