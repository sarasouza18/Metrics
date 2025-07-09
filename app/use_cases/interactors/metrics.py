class MetricsInteractor:
    async def get_user_metrics(self, user_id: str) -> dict:
        # fake response por enquanto
        return {
            "userId": user_id,
            "metrics": {
                "sharesCount": 5,
                "likeCount": 25
            },
            "chartData": {
                "pieChart": [
                    {"category": "positive", "value": 20, "percentage": 80},
                    {"category": "negative", "value": 5, "percentage": 20}
                ]
            },
            "lastUpdated": "2025-07-09T18:00:00Z"
        }
