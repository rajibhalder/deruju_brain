import hashlib
from datetime import datetime

from pymongo import MongoClient

from config import Config
from logger import logger


def make_signature(signal_doc):
    text = (
    signal_doc.category
    + "|"
    + signal_doc.title
    + "|"
    + ",".join(
    sorted(signal_doc.affected_entities[:5])
    )
    )

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


class SignalStore:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DB]
        self.collection = self.db["premium_signals"]

    def save(self, signal_doc):
        signature = make_signature(signal_doc)
        existing = self.collection.find_one(
            {"_signature": signature}
        )

        now = datetime.utcnow()

        if existing:
            seen_count = existing.get(
                "seen_count",
                1
            ) + 1

            novelty_score = max(
                5,
                round(100 / seen_count, 1)
            )

            momentum_score = min(
                100,
                seen_count * 12
            )

            trend_direction = (
                "RISING"
                if seen_count >= 3
                else "STABLE"
            )

            status = (
                "ACTIVE"
                if seen_count >= 3
                else "EMERGING"
            )

            doc = signal_doc.to_dict()
            doc.pop("_id", None)

            self.collection.update_one(
                {
                "_signature": signature
                },
                {
                "$set": {
                    **doc,
                    "_signature": signature,
                    "last_seen_at": now,
                    "seen_count": seen_count,
                    "novelty_score": novelty_score,
                    "momentum_score": momentum_score,
                    "trend_direction": trend_direction,
                    "status": status
                }
                }
            )

            logger.info(
                f"saved signal: {signal_doc.title}"
            )

            return {
                "trend_direction": trend_direction,
                "novelty_score": novelty_score,
                "momentum_score": momentum_score,
                "status": status
            }

        else:
            doc = signal_doc.to_dict()

            doc["_signature"] = signature
            doc["first_seen_at"] = now
            doc["last_seen_at"] = now
            doc["seen_count"] = 1
            doc["novelty_score"] = 100
            doc["momentum_score"] = 10
            doc["trend_direction"] = "NEW"
            doc["status"] = "NEW"

            self.collection.insert_one(doc)

            logger.info(
                f"saved signal: {signal_doc.title}"
            )

            return {
                "trend_direction": "NEW",
                "novelty_score": 100,
                "momentum_score": 10,
                "status": "NEW"
            }
