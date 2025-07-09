import boto3
import os
import time

dynamodb = boto3.client(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url=os.getenv("DYNAMODB_ENDPOINT", "http://localhost:8001"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "local"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "local")
)

def create_user_metrics_table():
    table_name = os.getenv("DYNAMODB_TABLE_NAME", "UserMetrics")

    existing_tables = dynamodb.list_tables()["TableNames"]
    if table_name in existing_tables:
        print(f"✅ Table '{table_name}' already exists.")
        return

    print(f"🚧 Creating table '{table_name}'...")
    dynamodb.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {"AttributeName": "user_id", "AttributeType": "S"}
        ],
        KeySchema=[
            {"AttributeName": "user_id", "KeyType": "HASH"}
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )

    print("⏳ Waiting for table to become ACTIVE...")
    while True:
        status = dynamodb.describe_table(TableName=table_name)["Table"]["TableStatus"]
        print(f" - Current status: {status}")
        if status == "ACTIVE":
            break
        time.sleep(1)

    print(f"✅ Table '{table_name}' is ACTIVE and ready.")

    # Insert sample item
    print("➕ Inserting sample user metrics for 'test-user'...")
    dynamodb.put_item(
        TableName=table_name,
        Item={
            'user_id': {'S': 'user-123'},
            'shares_count': {'N': '0'},
            'like_count': {'N': '0'},
            'positive_comment_count': {'N': '0'},
            'pie_chart': {'L': []},
            'last_updated': {'S': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        }
    )

    dynamodb.put_item(
        TableName=table_name,
        Item={
            'user_id': {'S': 'test-user'},
            'shares_count': {'N': '5'},
            'like_count': {'N': '25'},
            'positive_comment_count': {'N': '10'},
            'pie_chart': {
                'L': [
                    {'M': {
                        'category': {'S': 'Positive'},
                        'value': {'N': '10'},
                        'percentage': {'N': '50.0'}
                    }},
                    {'M': {
                        'category': {'S': 'Neutral'},
                        'value': {'N': '10'},
                        'percentage': {'N': '50.0'}
                    }}
                ]
            },
            'last_updated': {'S': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        }
    )
    print("✅ Sample data inserted successfully.")

if __name__ == "__main__":
    create_user_metrics_table()
