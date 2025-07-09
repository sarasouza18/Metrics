from datetime import datetime
from typing import Optional

from app.domain.entities import UserMetrics
from app.domain.exceptions import MetricsNotFoundError
from app.use_cases.metrics_interface import MetricsRepositoryInterface, MetricsPresenterInterface
from infrastructure.repositories.redis_cache import RedisCache


class MetricsInteractor:
    def __init__(
        self,
        repository: MetricsRepositoryInterface,
        presenter: MetricsPresenterInterface,
        cache: Optional[RedisCache] = None,
    ):
        self.repository = repository
        self.presenter = presenter
        self.cache = cache

    async def get_user_metrics(self, user_id: str) -> dict:
        # Attempt to fetch from cache
        if self.cache is not None:
            cached = await self.cache.get(user_id)
            if cached:
                return cached

        # Fetch raw metrics from repository (synchronous call)
        metrics = self.repository.get_user_metrics(user_id)
        if not metrics:
            raise MetricsNotFoundError()

        # Format the response
        last_updated = datetime.utcnow()
        result = self.presenter.present(
            metrics,
            user_id=user_id,
            last_updated=last_updated,
        )

        # Save in cache for future requests
        if self.cache is not None:
            await self.cache.set(user_id, result, ttl=60)

        return result
