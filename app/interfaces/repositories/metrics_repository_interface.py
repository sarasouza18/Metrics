# app/interfaces/repositories/metrics_repository_interface.py

from abc import ABC, abstractmethod

class MetricsRepositoryInterface(ABC):
    @abstractmethod
    async def get_user_metrics(self, user_id: str) -> dict:
        """
        Returns a dictionary containing:
        {
            "likeCount": int,
            "sharesCount": int,
            "sentiments": {
                "positive": int,
                "negative": int,
                ...
            }
        }
        """
        pass
