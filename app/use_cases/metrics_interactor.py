# app/use_cases/metrics_interactor.py

from app.domain.entities import UserMetrics
from app.domain.exceptions import MetricsNotFoundError
from app.use_cases.metrics_interface import MetricsRepositoryInterface, MetricsPresenterInterface
from infrastructure.repositories.redis_cache import RedisCache
from datetime import datetime

class MetricsInteractor:
    def __init__(
        self,
        repository: MetricsRepositoryInterface,
        presenter: MetricsPresenterInterface,
        cache: RedisCache
    ):
        self.repository = repository
        self.presenter = presenter
        self.cache = cache

    async def get_user_metrics(self, user_id: str) -> dict:
        # 🔁 Check cache first
        cached = await self.cache.get(user_id)
        if cached:
            return cached

        # 🧮 Aggregate from repository
        metrics = await self.repository.get_user_metrics(user_id)
        if not metrics:
            raise MetricsNotFoundError()

        # 🧾 Format using presenter
        last_updated = datetime.utcnow()
        result = self.presenter.present(metrics, user_id=user_id, last_updated=last_updated)

        # 💾 Save in cache with TTL
        await self.cache.set(user_id, result, ttl=60)

        return result
