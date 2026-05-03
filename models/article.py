from typing import List, Optional
from pydantic import BaseModel

class Entity(BaseModel):
    text: str
    label: str

class Article(BaseModel):
    id: str
    url: str
    title: str = ""
    summary: str = ""
    text: str = ""
    category: str = "general"
    source: str = ""
    published: Optional[str] = None
    entities: List[Entity] = []
    embedding: Optional[List[float]] = None


def content(self):
    if self.summary:
        return f"{self.title}\n{self.summary}"
    return f"{self.title}\n{self.text[:1500]}"
