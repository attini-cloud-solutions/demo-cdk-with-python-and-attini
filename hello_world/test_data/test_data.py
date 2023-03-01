import os
import boto3

dynamodb_client = boto3.client('dynamodb')


def lambda_handler(event, context):
    dynamodb_client.update_item(
        TableName=os.environ["DATABASE_NAME"],
        Key={
            'Id': {
                'S': 'my-id'
            }
        },
        AttributeUpdates={
            'message': {
                'Value': {
                    'S': 'hello-world'
                }
            }
        },
    )

    return "Test data created"
