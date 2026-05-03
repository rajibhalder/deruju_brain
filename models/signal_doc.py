from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import uuid

@dataclass
class SignalDoc:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    rank_score: float = 0.0

    category: str = ""
    title: str = ""
    summary: str = ""

    signal_type: str = ""
    importance: int = 0
    confidence: float = 0.0
    impact_window: str = ""

    affected_entities: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    action_ideas: List[str] = field(default_factory=list)

    source_cluster_size: int = 0
    why_it_matters: str = ""

    first_seen_at: datetime = field(default_factory=datetime.utcnow)
    last_seen_at: datetime = field(default_factory=datetime.utcnow)
    seen_count: int = 1
    trend_direction: str = "NEW"
    momentum_score: float = 0.0
    novelty_score: float = 100.0
    status: str = "NEW"

    urgency: str = "MEDIUM"
    india_relevance: int = 5
    market_impact: str = ""
    opportunity_score: int = 0
    risk_score: int = 0
    watch_tags: list = field(default_factory=list)
    affected_sectors: list = field(default_factory=list)

    def to_dict(self):
        return {
            "_id": self.id,
            "created_at": self.created_at,
            "category": self.category,
            "title": self.title,
            "summary": self.summary,
            "signal_type": self.signal_type,
            "importance": self.importance,
            "confidence": self.confidence,
            "impact_window": self.impact_window,
            "affected_entities": self.affected_entities,
            "tags": self.tags,
            "action_ideas": self.action_ideas,
            "source_cluster_size": self.source_cluster_size,
            "why_it_matters": self.why_it_matters,
            "first_seen_at": self.first_seen_at,
            "last_seen_at": self.last_seen_at,
            "seen_count": self.seen_count,
            "status": self.status,
            "trend_direction": self.trend_direction,
            "momentum_score": self.momentum_score,
            "novelty_score": self.novelty_score,
            "rank_score": self.rank_score,
            "urgency": self.urgency,
            "india_relevance": self.india_relevance,
            "market_impact": self.market_impact,
            "opportunity_score": self.opportunity_score,
            "risk_score": self.risk_score,
            "watch_tags": self.watch_tags,
            "affected_sectors": self.affected_sectors,
        }
