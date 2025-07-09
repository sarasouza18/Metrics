# app/interfaces/presenters/metrics_presenter.py

from abc import ABC, abstractmethod
from datetime import datetime
from app.domain.entities import UserMetrics


class MetricsPresenterInterface(ABC):
    @abstractmethod
    def present(self, metrics: UserMetrics, user_id: str, last_updated: datetime) -> dict:
        pass


class MetricsPresenter(MetricsPresenterInterface):
    def present(self, metrics: UserMetrics, user_id: str, last_updated: datetime) -> dict:
        return {
            "user_id": user_id,
            "shares_count": metrics.shares_count,
            "like_count": metrics.like_count,
            "positive_comment_count": metrics.positive_comment_count,
            "pie_chart": [
                {
                    "category": item.category,
                    "value": item.value,
                    "percentage": item.percentage,
                }
                for item in metrics.pie_chart
            ],
            "last_updated": last_updated.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
