# app/interfaces/presenters/metrics_presenter.py
from app.use_cases.metrics_interface import MetricsPresenterInterface
from app.domain.entities import UserMetrics

class MetricsPresenter(MetricsPresenterInterface):
    def present(self, metrics: UserMetrics) -> dict:
        return metrics.to_api_response()