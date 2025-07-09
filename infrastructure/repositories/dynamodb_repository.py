# infrastructure/repositories/dynamodb_repository.py
import boto3
from app.domain.entities import UserMetrics, PieChartItem
from app.use_cases.metrics_interface import MetricsRepositoryInterface
from app.domain.exceptions import MetricsNotFoundError
from datetime import datetime

class DynamoDBMetricsRepository(MetricsRepositoryInterface):
    def __init__(self):
        self.client = boto3.client('dynamodb')
        self.table_name = 'user_metrics'

    def get_user_metrics(self, user_id: str) -> UserMetrics:
        response = self.client.get_item(
            TableName=self.table_name,
            Key={'user_id': {'S': user_id}}
        )
        
        if 'Item' not in response:
            raise MetricsNotFoundError()
        
        item = response['Item']
        return UserMetrics(
            user_id=user_id,
            shares_count=int(item['shares_count']['N']),
            like_count=int(item['like_count']['N']),
            positive_comment_count=int(item['positive_comment_count']['N']),
            pie_chart=[
                PieChartItem(
                    category=p['category']['S'],
                    value=int(p['value']['N']),
                    percentage=float(p['percentage']['N'])
                ) for p in item['pie_chart']['L']
            ],
            last_updated=datetime.strptime(item['last_updated']['S'], '%Y-%m-%dT%H:%M:%SZ')
        )