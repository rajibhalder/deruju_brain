import hashlib
import json
import re
import requests

from pymongo import MongoClient

from config import Config
from logger import logger

class ClusterReasoner:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DB]
        self.cache = self.db["brain_cache"]

    def _extract_json(self, content: str):
        if not content:
            raise ValueError("empty response")

        content = content.strip()

        content = re.sub(
            r"^json\s*",
            "",
            content,
            flags=re.IGNORECASE
        )

        content = re.sub(
            r"^\s*",
            "",
            content
        )

        content = re.sub(
            r"\s*$",
            "",
            content
        )

        start = content.find("{")
        end = content.rfind("}")

        if start >= 0 and end > start:
            content = content[start:end + 1]

        return json.loads(content)

    def _make_cluster_hash(self, titles, top_entities):
        raw = (
            "|".join(sorted(titles[:10]))
            + "|"
            + "|".join(sorted(top_entities[:10]))
        )

        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()

    def reason(self, cluster, top_entities):
        titles = [
            a.title
            for a in cluster.articles[:10]
            if a.title
        ]

        cluster_hash = self._make_cluster_hash(
            titles,
            top_entities
        )

        cached = self.cache.find_one(
            {"_id": cluster_hash}
        )

        if cached:
            logger.info(
                f"brain cache hit={cluster_hash[:8]}"
            )
            return cached["reasoning"]

        prompt = f"""
    `

    You are an expert intelligence analyst.

    Analyze this news cluster.

    Cluster size: {cluster.size}

    Titles:
    {json.dumps(titles, indent=2)}

    Top entities:
    {json.dumps(top_entities, indent=2)}

    Return ONLY JSON.

    {{
    "category": "",
    "theme": "",
    "signal_type": "",
    "importance": 0,
    "confidence": 0.0,
    "impact_window": "",
    "why_it_matters": "",
    "action_ideas": []
    }}
    """


        payload = {
            "model": Config.DEEPSEEK_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2,
            "response_format": {
                "type": "json_object"
            }
        }

        headers = {
            "Authorization": (
                f"Bearer {Config.DEEPSEEK_API_KEY}"
            ),
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                "https://api.deepseek.com/chat/completions",
                json=payload,
                headers=headers,
                timeout=60
            )

            response.raise_for_status()

            content = response.json()[
                "choices"
            ][0]["message"]["content"]

            reasoning = self._extract_json(content)

            self.cache.insert_one({
                "_id": cluster_hash,
                "reasoning": reasoning
            })

            logger.info(
                f"brain cache saved={cluster_hash[:8]}"
            )

            return reasoning

        except Exception as ex:
            logger.exception(
                f"reasoning failed: {ex}"
            )

            return {
                "category": "General",
                "theme": "Emerging trend",
                "signal_type": "trend",
                "importance": 5,
                "confidence": 0.5,
                "impact_window": "1-4 weeks",
                "why_it_matters":
                    "Unable to classify automatically.",
                "action_ideas": [
                    "Monitor developments"
                ]
            }
