# infrastructure/api/dependencies.py

from app.use_cases.metrics_interactor import MetricsInteractor
from  app.interfaces.presenters.metrics_presenter import MetricsPresenter
from infrastructure.repositories.dynamodb_repository import DynamoDBMetricsRepository
from infrastructure.repositories.redis_cache import RedisCache

async def get_metrics_interactor() -> MetricsInteractor:
    repository = DynamoDBMetricsRepository()
    presenter = MetricsPresenter()
    cache = RedisCache()
    return MetricsInteractor(repository, presenter, cache)
