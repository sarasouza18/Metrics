# infrastructure/api/dependencies.py
from fastapi import Depends
from app.use_cases.metrics_interactor import MetricsInteractor
from infrastructure.repositories.dynamodb_repository import DynamoDBMetricsRepository
from app.interfaces.presenters.metrics_presenter import MetricsPresenter

def get_metrics_interactor():
    repository = DynamoDBMetricsRepository()
    presenter = MetricsPresenter()
    return MetricsInteractor(repository, presenter)