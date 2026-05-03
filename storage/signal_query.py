from pymongo import MongoClient

from config import Config

class SignalQuery:
	def __init__(self):
		self.client = MongoClient(Config.MONGO_URI)
		self.db = self.client[Config.MONGO_DB]
		self.collection = self.db["premium_signals"]

	def top_signals(self, limit=20):
		return list(
			self.collection.find()
			.sort("rank_score", -1)
			.limit(limit)
		)

	def by_trend(self, trend):
		return list(
			self.collection.find(
				{
					"trend_direction": trend
				}
			).sort("rank_score", -1)
		)

	def by_sector(self, sector):
		return list(
			self.collection.find(
				{
					"affected_sectors": sector
				}
			).sort("rank_score", -1)
		)

	def urgent_india(self):
		return list(
			self.collection.find(
				{
					"india_relevance": {
						"$gte": 7
					}
				}
			).sort("rank_score", -1)
		)
