# app/use_cases/metrics_interface.py

from abc import ABC, abstractmethod
from app.domain.entities import UserMetrics

class MetricsRepositoryInterface(ABC):
    @abstractmethod
    def get_user_metrics(self, user_id: str) -> UserMetrics:
        """
        Returns a UserMetrics domain entity for a given user.
        """
        pass

class MetricsPresenterInterface(ABC):
    @abstractmethod
    def present(self, metrics: UserMetrics) -> dict:
        """
        Converts the UserMetrics entity into a dictionary response
        following the API format.
        """
        pass
