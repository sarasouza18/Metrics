# app/use_cases/metrics_interface.py
from abc import ABC, abstractmethod
from app.domain.entities import UserMetrics

class MetricsRepositoryInterface(ABC):
    @abstractmethod
    def get_user_metrics(self, user_id: str) -> UserMetrics:
        pass

class MetricsPresenterInterface(ABC):
    @abstractmethod
    def present(self, metrics: UserMetrics) -> dict:
        pass