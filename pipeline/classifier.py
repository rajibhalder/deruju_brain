from collections import Counter, defaultdict
import re

RULES = {
"weather": {
"positive": ["heatwave", "weather", "rain", "storm", "cyclone", "flood", "imd", "monsoon"],
"negative": []
},
"geopolitics": {
"positive": ["war", "strike", "military", "terror", "border", "missile", "sanction"],
"negative": ["movie", "cricket", "garden"]
},
"economy": {
"positive": ["market", "stock", "inflation", "rbi", "salary", "economy", "gdp", "tax"],
"negative": ["match", "actor"]
},
"technology": {
"positive": ["ai", "openai", "nvidia", "chip", "semiconductor", "robotics", "software"],
"negative": ["dog", "garden", "actor", "marathon"]
},
"career": {
"positive": ["job", "jobs", "exam", "education", "career", "hiring", "recruitment"],
"negative": []
},
"low_value": {
"positive": ["ipl", "cricket", "movie", "actor", "celebrity", "box office"],
"negative": []
}
}

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def classify_cluster(cluster):
    tokens = []
    for article in cluster.articles[:20]:
        tokens.extend(normalize(article.title).split())

        for e in article.entities[:10]:
            if e.text:
                tokens.extend(normalize(e.text).split())

    freq = Counter(tokens)
    scores = defaultdict(int)

    for category, rule in RULES.items():
        for word in rule["positive"]:
            scores[category] += freq[word] * 3

        for word in rule["negative"]:
            scores[category] -= freq[word] * 2

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    best_cat, best_score = ranked[0]

    if best_score <= 0:
        return {
            "category": "general",
            "confidence": 0.0,
            "scores": dict(scores)
        }

    total = sum(max(0, v) for v in scores.values())
    confidence = round(best_score / total, 2) if total else 0.0

    if confidence < 0.45:
        best_cat = "general"

    return {
        "category": best_cat,
        "confidence": confidence,
        "scores": dict(scores)
    }
