"""
Natural Language Processing and semantic signal extraction for topic discovery.
"""

from __future__ import annotations
from collections import Counter
import html
import re
from typing import Dict, List, Set

from market_research.models import RawSignal, TopicCluster

STOP_WORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "can't", "cannot", "could",
    "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from",
    "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself",
    "him", "himself", "his", "how", "i", "if", "in", "into", "is", "isn't", "it",
    "its", "itself", "just", "me", "more", "most", "my", "myself", "no", "nor", "not",
    "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves",
    "out", "over", "own", "same", "she", "should", "so", "some", "such", "than", "that",
    "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they",
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why",
    "with", "would", "you", "your", "yours", "yourself", "yourselves",
    "show", "hn", "ask", "tell", "using", "use", "used", "get", "got", "also", "one",
    "two", "new", "like", "make", "made", "want", "see", "look", "looking", "way",
    "first", "good", "well", "much", "many", "even", "still", "people", "everyone"
}

PAIN_TOKENS: Set[str] = {
    "issue", "issues", "problem", "problems", "bug", "bugs", "broken", "difficult",
    "hard", "frustrated", "frustrating", "hate", "struggle", "struggling", "slow",
    "expensive", "costly", "confusing", "nightmare", "fail", "failing", "pain",
    "painful", "error", "errors", "limitations", "stuck", "bottleneck", "missing"
}

BUYER_TOKENS: Set[str] = {
    "best", "vs", "versus", "compare", "comparison", "review", "reviews", "alternative",
    "alternatives", "pricing", "price", "cost", "buy", "purchase", "software", "tool",
    "tools", "platform", "solution", "service", "recommend", "recommendation", "hire"
}


class TopicExtractor:
    """Analyzes raw signals to extract themes, sentiment, pain points, and clusters."""

    def tokenize(self, text: str) -> List[str]:
        """Convert text into normalized words without punctuation."""
        unescaped = html.unescape(text)
        return [w.lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', unescaped)]

    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """Extract dominant meaningful keywords."""
        tokens = [t for t in self.tokenize(text) if t not in STOP_WORDS]
        counts = Counter(tokens)
        return [k for k, _ in counts.most_common(top_n)]

    def extract_questions(self, text: str) -> List[str]:
        """Find explicit questions asked by users."""
        sentences = re.split(r'\.|\n|\!|\?', text)
        questions: List[str] = []
        for s in sentences:
            cleaned = s.strip()
            if not cleaned:
                continue
            lower = cleaned.lower()
            if any(lower.startswith(q) for q in ["how", "why", "what", "is there", "can i", "where", "which", "are there"]):
                questions.append(cleaned + "?")
        return questions

    def calculate_pain_density(self, text: str) -> float:
        """Calculate the proportion of pain/frustration words in text."""
        tokens = self.tokenize(text)
        if not tokens:
            return 0.0
        pain_count = sum(1 for t in tokens if t in PAIN_TOKENS)
        # Normalized score between 0.0 and 1.0
        ratio = (pain_count * 15) / len(tokens)
        return min(1.0, round(ratio, 3))

    def calculate_buyer_intent(self, text: str) -> float:
        """Calculate commercial and buyer intent strength."""
        tokens = self.tokenize(text)
        if not tokens:
            return 0.0
        buyer_count = sum(1 for t in tokens if t in BUYER_TOKENS)
        ratio = (buyer_count * 12) / len(tokens)
        return min(1.0, round(ratio, 3))

    def cluster_signals(self, signals: List[RawSignal]) -> List[TopicCluster]:
        """Cluster raw signals into thematic topics based on keyword affinity."""
        clusters_map: Dict[str, List[RawSignal]] = {}

        for sig in signals:
            combined_text = f"{sig.title} {sig.body}"
            keywords = self.extract_keywords(combined_text, top_n=3)
            primary_topic = keywords[0] if keywords else "general"

            # Normalize primary topic name
            cluster_name = primary_topic.capitalize()
            if cluster_name not in clusters_map:
                clusters_map[cluster_name] = []
            clusters_map[cluster_name].append(sig)

        results: List[TopicCluster] = []
        for name, sig_list in clusters_map.items():
            all_text = " ".join([f"{s.title} {s.body}" for s in sig_list])
            keywords = self.extract_keywords(all_text, top_n=8)
            pain_density = self.calculate_pain_density(all_text)

            questions: List[str] = []
            for s in sig_list:
                questions.extend(self.extract_questions(s.title))
                questions.extend(self.extract_questions(s.body))

            # Deduplicate questions
            unique_questions = list(dict.fromkeys(questions))[:5]

            cluster = TopicCluster(
                name=name,
                keywords=keywords,
                signals=sig_list,
                total_mentions=len(sig_list),
                sentiment_score=0.1,  # baseline
                pain_density=pain_density,
                questions=unique_questions,
            )
            results.append(cluster)

        # Sort clusters by mention count descending
        results.sort(key=lambda c: c.total_mentions, reverse=True)
        return results
