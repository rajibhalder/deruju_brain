import hashlib

from models import signal_doc
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

        if existing:
            self.collection.update_one(
                {"_signature": signature},
                {
                    "$set": {
                        **signal_doc.to_dict(),
                        "_signature": signature
                    },
                    "$inc": {
                        "seen_count": 1
                    },
                    "$currentDate": {
                        "last_seen_at": True,
                        "updated_at": True
                    }
                }
            )
        else:
            doc = signal_doc.to_dict()
            doc["_signature"] = signature

            self.collection.insert_one(doc)

        logger.info(
            f"saved signal: {signal_doc.title}"
        )
