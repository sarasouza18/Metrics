# app/use_cases/metrics_interactor.py
from app.domain.entities import UserMetrics
from app.use_cases.metrics_interface import MetricsRepositoryInterface, MetricsPresenterInterface

class MetricsInteractor:
    def __init__(
        self,
        repository: MetricsRepositoryInterface,
        presenter: MetricsPresenterInterface
    ):
        self.repository = repository
        self.presenter = presenter

    def get_user_metrics(self, user_id: str) -> dict:
        metrics = self.repository.get_user_metrics(user_id)
        return self.presenter.present(metrics)