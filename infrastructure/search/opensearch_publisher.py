# infrastructure/search/opensearch_publisher.py

from opensearchpy import OpenSearch
import os

class OpenSearchPublisher:
    def __init__(self):
        self.client = OpenSearch(
            hosts=[{'host': os.getenv("OPENSEARCH_HOST", "localhost"), 'port': int(os.getenv("OPENSEARCH_PORT", 9200))}],
            http_auth=(os.getenv("OPENSEARCH_USER", "admin"), os.getenv("OPENSEARCH_PASS", "admin")),
            use_ssl=False,
            verify_certs=False
        )
        self.index_name = os.getenv("OPENSEARCH_INDEX", "user-metrics")

    async def publish_metrics(self, user_id: str, metrics: dict):
        doc_id = f"user-{user_id}"
        self.client.index(index=self.index_name, id=doc_id, body=metrics)
