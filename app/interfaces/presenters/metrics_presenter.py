# app/interfaces/presenters/metrics_presenter.py

from app.use_cases.metrics_interface import MetricsPresenterInterface
from datetime import datetime

class MetricsPresenter(MetricsPresenterInterface):
    def present(self, metrics: dict, user_id: str, last_updated: datetime) -> dict:
        # Expects metrics to contain: likeCount, sharesCount, sentiments (dict)
        sentiments = metrics.get("sentiments", {})
        total = sum(sentiments.values())

        pie_chart = [
            {
                "category": key,
                "value": value,
                "percentage": round((value / total) * 100, 2) if total > 0 else 0
            }
            for key, value in sentiments.items()
        ]

        return {
            "userId": user_id,
            "metrics": {
                "sharesCount": metrics.get("sharesCount", 0),
                "likeCount": metrics.get("likeCount", 0),
            },
            "chartData": {
                "pieChart": pie_chart
            },
            "lastUpdated": last_updated.isoformat()
        }
