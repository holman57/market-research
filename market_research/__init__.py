"""
Market Research Engine
~~~~~~~~~~~~~~~~~~~~~~
A web crawler, topic scoring, and niche discovery system for automated
market research and content ideation.
"""

__version__ = "0.1.0"
__author__ = "Luke Holman"

from market_research.models import (
    ContentBrief,
    InquiryDossier,
    NicheOpportunity,
    RawSignal,
    SourceType,
    TopicCluster,
    TopicScore,
)
from market_research.crawler.web_crawler import WebCrawler
from market_research.analysis.nlp import TopicExtractor
from market_research.analysis.trends import TrendAnalyzer
from market_research.scoring.scorer import TopicScorer
from market_research.discovery.niche_finder import NicheFinder
from market_research.discovery.content_generator import ContentGenerator
from market_research.inquiry.topical_inquiry import TopicalInquiryEngine

__all__ = [
    "ContentBrief",
    "ContentGenerator",
    "InquiryDossier",
    "NicheFinder",
    "NicheOpportunity",
    "RawSignal",
    "SourceType",
    "TopicCluster",
    "TopicExtractor",
    "TopicScore",
    "TopicScorer",
    "TopicalInquiryEngine",
    "TrendAnalyzer",
    "WebCrawler",
]
