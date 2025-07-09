import os
from datetime import datetime
import boto3
from app.domain.entities import UserMetrics, PieChartItem
from app.use_cases.metrics_interface import MetricsRepositoryInterface
from app.domain.exceptions import MetricsNotFoundError


class DynamoDBMetricsRepository(MetricsRepositoryInterface):
    def __init__(self):
        self.client = boto3.client(
            'dynamodb',
            endpoint_url=os.getenv("DYNAMODB_ENDPOINT", "http://localhost:8001"),
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "local"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "local"),
        )
        self.table_name = os.getenv("DYNAMODB_TABLE_NAME", "UserMetrics")

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
                    category=entry['M']['category']['S'],
                    value=int(entry['M']['value']['N']),
                    percentage=float(entry['M']['percentage']['N'])
                ) for entry in item['pie_chart']['L']
            ],
            last_updated=datetime.strptime(item['last_updated']['S'], "%Y-%m-%dT%H:%M:%SZ")
        )
