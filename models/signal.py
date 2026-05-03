from typing import List
from pydantic import BaseModel
from datetime import datetime

class PremiumSignal(BaseModel):
    title: str
    summary: str
    category: str
    signal_type: str
    confidence: float
    importance: int
    impact_window: str
    affected_entities: List[str]
    tags: List[str]
    why_it_matters: str
    action_ideas: List[str]
    created_at: datetime
