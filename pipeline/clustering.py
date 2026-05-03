import numpy as np
import hdbscan

from models.cluster import Cluster
from logger import logger

def cluster_articles(articles):
    logger.info("preparing vectors...")

    usable_articles = [
        a for a in articles
        if a.embedding and len(a.embedding) > 0
    ]

    if not usable_articles:
        logger.warning("no embedded articles found")
        return []

    vectors = np.array(
        [a.embedding for a in usable_articles],
        dtype=np.float32
    )

    logger.info(f"clustering {len(usable_articles)} articles...")

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=4,
        min_samples=2,
        cluster_selection_epsilon=0.15,
        metric="euclidean"
    )


    labels = clusterer.fit_predict(vectors)

    grouped = {}

    for label, article in zip(labels, usable_articles):
        if label == -1:
            continue

        grouped.setdefault(int(label), []).append(article)

    clusters = []

    for cid, group in grouped.items():
        clusters.append(
            Cluster(
                cluster_id=cid,
                articles=group,
                size=len(group)
            )
        )

    logger.info(f"generated {len(clusters)} clusters")

    return sorted(
        clusters,
        key=lambda x: x.size,
        reverse=True
    )
