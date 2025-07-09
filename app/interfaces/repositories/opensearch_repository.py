# infrastructure/repositories/opensearch_repository.py

from app.interfaces.repositories.metrics_repository_interface import MetricsRepositoryInterface
from opensearchpy import OpenSearch
from typing import Dict
import os

class OpenSearchRepository(MetricsRepositoryInterface):
    def __init__(self):
        self.client = OpenSearch(
            hosts=[{"host": os.getenv("OPENSEARCH_HOST", "localhost"), "port": 9200}],
            http_compress=True,
            use_ssl=False,
            verify_certs=False
        )
        self.index_name = os.getenv("OPENSEARCH_INDEX", "metrics-comments")

    async def get_user_metrics(self, user_id: str) -> Dict:
        query = {
            "query": {
                "term": {
                    "user_id.keyword": user_id
                }
            },
            "aggs": {
                "sentiments": {
                    "terms": {
                        "field": "sentiment.keyword"
                    }
                }
            },
            "size": 10000  # pode ser ajustado se necessário
        }

        try:
            response = self.client.search(index=self.index_name, body=query)
        except Exception as e:
            print(f"OpenSearch query failed: {e}")
            return {}

        hits = response.get("hits", {}).get("hits", [])
        aggregations = response.get("aggregations", {}).get("sentiments", {}).get("buckets", [])

        like_count = sum(hit["_source"].get("likes", 0) for hit in hits if "likes" in hit["_source"])
        shares_count = sum(hit["_source"].get("shares", 0) for hit in hits if "shares" in hit["_source"])

        sentiments = {
            bucket["key"]: bucket["doc_count"]
            for bucket in aggregations
        }

        return {
            "likeCount": like_count,
            "sharesCount": shares_count,
            "sentiments": sentiments
        }
