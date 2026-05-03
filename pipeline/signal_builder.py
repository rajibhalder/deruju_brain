from datetime import datetime
from models.signal_doc import SignalDoc

def build_signal(cluster, top_entities, reasoning):
        return SignalDoc(
            created_at=datetime.utcnow(),
            category=reasoning.get("category", "General"),
            title=reasoning.get("theme", "Emerging trend"),
            summary=reasoning.get("why_it_matters", ""),
            signal_type=reasoning.get("signal_type", "trend"),
            importance=int(reasoning.get("importance", 5)),
            confidence=float(reasoning.get("confidence", 0.5)),
            impact_window=reasoning.get("impact_window", "1-4 weeks"),
            affected_entities=top_entities,
            tags=top_entities[:5],
            action_ideas=reasoning.get("action_ideas", []),
            source_cluster_size=cluster.size,
            why_it_matters=reasoning.get("why_it_matters", ""),
            urgency=reasoning.get("urgency", "MEDIUM"),
            india_relevance=reasoning.get("india_relevance", 5),
            market_impact=reasoning.get("market_impact", ""),
            opportunity_score=reasoning.get("opportunity_score", 0),
            risk_score=reasoning.get("risk_score", 0),
            watch_tags=reasoning.get("watch_tags", []),
            affected_sectors=reasoning.get("affected_sectors", []),
        )