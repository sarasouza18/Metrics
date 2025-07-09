import boto3
import os
from datetime import datetime

def seed():
    # Configurar cliente
    client = boto3.client(
        'dynamodb',
        endpoint_url=os.getenv("DYNAMODB_ENDPOINT", "http://dynamodb:8000"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "local"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "local"),
    )

    # Dados a serem inseridos
    item = {
        'user_id': {'S': '1'},
        'shares_count': {'N': '10'},
        'like_count': {'N': '50'},
        'positive_comment_count': {'N': '7'},
        'pie_chart': {'L': [
            {'M': {
                'category': {'S': 'positive'},
                'value': {'N': '7'},
                'percentage': {'N': '100.0'}
            }}
        ]},
        'last_updated': {'S': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
    }

    # Inserir item na tabela
    response = client.put_item(
        TableName="UserMetrics",
        Item=item
    )

    print("✅ Seed completed:", response)

if __name__ == "__main__":
    seed()
