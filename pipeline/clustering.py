import re
from collections import Counter, defaultdict

import numpy as np
import hdbscan

from models.cluster import Cluster
from logger import logger

STOP_WORDS = {
"the", "a", "an", "and", "or", "of", "to",
"in", "on", "for", "with", "at", "by",
"after", "amid", "from", "into"
}

def extract_keywords(title):
    if not title:
        return []
    words = re.findall(
        r"[A-Za-z]{4,}",
        title.lower()
    )

    return [
        w for w in words
        if w not in STOP_WORDS
    ]


def split_if_mixed(group):
    keyword_count = Counter()
    article_keywords = []

    for article in group:
        kws = extract_keywords(article.title)
        article_keywords.append((article, kws))
        keyword_count.update(kws)

    dominant = {
        k
        for k, _ in keyword_count.most_common(8)
    }

    buckets = defaultdict(list)

    for article, kws in article_keywords:
        assigned = "misc"

        for kw in kws:
            if kw in dominant:
                assigned = kw
                break

        buckets[assigned].append(article)

    # if meaningful split exists
    valid_groups = [
        g for g in buckets.values()
        if len(g) >= 3
    ]

    if len(valid_groups) >= 2:
        return valid_groups

    return [group]


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

    logger.info(
        f"clustering {len(usable_articles)} articles..."
    )

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

        grouped.setdefault(
            int(label),
            []
        ).append(article)

    clusters = []
    cid = 0

    for _, group in grouped.items():
        split_groups = split_if_mixed(group)

        for sg in split_groups:
            clusters.append(
                Cluster(
                    cluster_id=cid,
                    articles=sg,
                    size=len(sg)
                )
            )
            cid += 1

    logger.info(
        f"generated {len(clusters)} clusters"
    )

    return sorted(
        clusters,
        key=lambda x: x.size,
        reverse=True
    )
