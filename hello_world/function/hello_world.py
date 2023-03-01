import json
import os
import boto3
from botocore.config import Config

dynamo_connection_config = Config(
    retries={
        'mode': 'standard'
    }
)

dynamodb_client = boto3.client("dynamodb", config=dynamo_connection_config)


def get_test_data(id):
    return dynamodb_client.get_item(
        TableName=os.environ["DATABASE_NAME"],
        Key={
            'Id': {
                'S': id,
            }
        },
    )["Item"]["message"]["S"]


def lambda_handler(event, context):
    print(f"Got event: {json.dumps(event)}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"{get_test_data('my-id')}"
        }),
    }
