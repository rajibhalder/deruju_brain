from datetime import datetime, timedelta
from pymongo import MongoClient
from config import Config
from models.article import Article
from logger import logger

class MongoStore:
    def __init__(self):
        logger.info("connecting mongodb...")

        self.client = MongoClient(
            Config.MONGO_URI,
            serverSelectionTimeoutMS=5000
        )

        self.client.admin.command("ping")
        logger.info("mongodb connected")

        self.db = self.client[Config.MONGO_DB]
        self.article_collection = self.db[Config.MONGO_ARTICLE_COLLECTION]
        self.signal_collection = self.db[Config.MONGO_SIGNAL_COLLECTION]

    def fetch_recent_articles(self):
        cutoff = datetime.utcnow() - timedelta(days=Config.LOOKBACK_DAYS)
        cutoff_str = cutoff.strftime("%Y-%m-%d")


        logger.info(f"fetching embedded articles since {cutoff_str}")

        cursor = self.article_collection.find(
            {
                "embedding": {"$exists": True, "$ne": None},
                "published": {"$gte": cutoff_str}
            }
        ).limit(Config.MAX_ARTICLES)

        articles = []

        for doc in cursor:
            try:
                entities = []

                for e in doc.get("entities", []):
                    if isinstance(e, dict):
                        text = e.get("text") or e.get("0") or ""
                        label = e.get("label") or e.get("1") or ""

                        if text:
                            entities.append({
                                "text": text,
                                "label": label
                            })

                article = Article(
                    id=str(doc["_id"]),
                    url=doc.get("url", ""),
                    title=doc.get("title") or "",
                    summary=doc.get("summary") or "",
                    text=doc.get("text") or "",
                    category=doc.get("category", "general"),
                    source=doc.get("source", ""),
                    published=doc.get("published"),
                    entities=entities,
                    embedding=doc.get("embedding")
                )

                articles.append(article)

            except Exception as ex:
                logger.warning(f"skipped bad document: {ex}")

        logger.info(f"loaded {len(articles)} embedded articles")
        return articles

def save_signal(self, signal):
    self.signal_collection.insert_one(signal.model_dump())
