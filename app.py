from logger import logger
from pipeline.fetcher import fetch_articles
from pipeline.clustering import cluster_articles
from pipeline.signal_builder import build_signal
from services.entity_cleaner import top_entities
from services.cluster_reasoner import ClusterReasoner
from storage.signal_store import SignalStore

ALLOWED_CATEGORIES = {
    "Geopolitical Conflict",
    "Politics & Governance",
    "Economy & Markets",
    "Financial Markets",
    "Technology & Innovation",
    "Technology & Consumer Electronics",
    "Climate & Weather",
    "Energy & Commodities",
    "Public Policy",
    "Education & Career",
    "Security & Counterterrorism",
    "Infrastructure & Urban Development",
    "Disaster and Accident",
    "Disaster & Emergency Response",
    "Domestic Political & Social Tensions",
    "Health & Public Safety"
}


def normalize_category(category: str):
    if not category:
        return "General"

    c = category.strip().lower()

    if "geopolitical" in c:
        return "Geopolitical Conflict"

    if "politic" in c or "governance" in c:
        return "Politics & Governance"

    if "financial" in c:
        return "Financial Markets"

    if "economy" in c or "market" in c:
        return "Economy & Markets"

    if "technology" in c or "consumer electronics" in c:
        return "Technology & Consumer Electronics"

    if "climate" in c or "weather" in c:
        return "Climate & Weather"

    if "energy" in c or "commodity" in c:
        return "Energy & Commodities"

    if "education" in c or "career" in c:
        return "Education & Career"

    if "security" in c or "counterterrorism" in c:
        return "Security & Counterterrorism"

    if "infrastructure" in c or "urban development" in c:
        return "Infrastructure & Urban Development"

    if "disaster" in c or "emergency" in c:
        return "Disaster & Emergency Response"

    if "health" in c or "public safety" in c:
        return "Health & Public Safety"

    if "policy" in c:
        return "Public Policy"

    return "Other"


def is_low_value_cluster(cluster):
    text = " ".join(
    [a.title.lower() for a in cluster.articles[:10] if a.title]
    )


    low_value_keywords = [
        "ipl",
        "cricket",
        "match",
        "movie",
        "actor",
        "actress",
        "celebrity",
        "box office",
        "gardening",
        "recipe"
    ]

    return any(word in text for word in low_value_keywords)


def main():
    logger.info("starting deruju brain")


    articles = fetch_articles()
    logger.info(f"articles fetched = {len(articles)}")

    clusters = cluster_articles(articles)
    logger.info(f"clusters formed = {len(clusters)}")

    reasoner = ClusterReasoner()
    signal_store = SignalStore()
    shown = 0

    for cluster in clusters:

        # cheap junk filter
        if is_low_value_cluster(cluster):
            logger.info(
                f"skipping low-value cluster size={cluster.size}"
            )
            continue

        entities = []

        for article in cluster.articles:
            for entity in article.entities:
                if entity.text:
                    entities.append(entity.text)

        best_entities = top_entities(entities)

        if not best_entities:
            best_entities = ["Unknown"]

        reasoning = reasoner.reason(
            cluster,
            best_entities
        )

        signal = build_signal(
            cluster,
            best_entities,
            reasoning
        )

        signal.category = normalize_category(signal.category)

        if signal.category not in ALLOWED_CATEGORIES:
            logger.info(f"skipping category={signal.category}")
            continue

        logger.info("===================================")
        logger.info(f"CATEGORY: {signal.category}")
        logger.info(f"TITLE: {signal.title}")
        logger.info(f"IMPORTANCE: {signal.importance}")
        logger.info(f"CONFIDENCE: {signal.confidence}")
        logger.info(f"WHY: {signal.why_it_matters}")
        logger.info(f"AFFECTED: {signal.affected_entities[:5]}")
        logger.info(f"ACTIONS: {signal.action_ideas}")

        signal.source_cluster_size = cluster.size
        life = signal_store.save(signal)

        logger.info(
            f"TREND={life['trend_direction']} "
            f"NOVELTY={life['novelty_score']} "
            f"MOMENTUM={life['momentum_score']} "
            f"RANK={life['rank_score']}"
        )

        shown += 1

        if shown >= 5:
            break

if __name__ == "__main__":
    main()
