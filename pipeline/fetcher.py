from storage.mongo import MongoStore

def fetch_articles():
    store = MongoStore()
    return store.fetch_recent_articles()
