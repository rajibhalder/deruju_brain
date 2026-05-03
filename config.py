import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB")
    MONGO_ARTICLE_COLLECTION = os.getenv("MONGO_ARTICLE_COLLECTION")
    MONGO_SIGNAL_COLLECTION = os.getenv("MONGO_SIGNAL_COLLECTION")

    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    LOOKBACK_DAYS = int(os.getenv("LOOKBACK_DAYS", "3"))
    MIN_CLUSTER_SIZE = int(os.getenv("MIN_CLUSTER_SIZE", "3"))
    MAX_ARTICLES = int(os.getenv("MAX_ARTICLES", "5000"))
