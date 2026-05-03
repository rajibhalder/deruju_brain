from typing import List
from pydantic import BaseModel
from models.article import Article

class Cluster(BaseModel):
    cluster_id: int
    articles: List[Article]
    keywords: List[str] = []
    size: int
