import boto3
from boto3.dynamodb.conditions import Key, Attr
from typing import Dict, Any, List
from app.service.database.base import BaseDatabase
from botocore.exceptions import ClientError
import os

class DynamoDBClient(BaseDatabase):
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=os.getenv("AWS_DYNAMO_DB_URL"),
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self.create_table_if_not_exists('cache')

    # This is used to create cache table when project initialize
    def create_table_if_not_exists(self, table_name: str):
        # Check if table already exists
        existing_tables = self.dynamodb.meta.client.list_tables()['TableNames']
        if table_name in existing_tables:
            print(f"Table '{table_name}' already exists.")
            return

        try:
            # Create table
            response = self.dynamodb.meta.client.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'filename',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'expired_at',
                        'KeyType': 'RANGE'  # Sort key (if needed)
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'filename',
                        'AttributeType': 'S'  # String
                    },
                    {
                        'AttributeName': 'expired_at',
                        'AttributeType': 'S'  # String (DateTime format as ISO 8601 string)
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            print(f"Table '{table_name}' created successfully.")
        except ClientError as e:
            print(f"Error creating table: {e}")

    # create record
    async def create(self, table_name: str, item: Dict[str, Any]) -> None:
        table = self.dynamodb.Table(table_name)
        try:
            table.put_item(Item=item)
        except Exception as e:
            print(f"Unexpected error: {e}")

    # update record 
    async def update(self, table_name: str, key: Dict[str, Any], updates: Dict[str, Any]) -> None:
        table = self.dynamodb.Table(table_name)
        update_expression = "set " + ", ".join([f"{k}= :{k}" for k in updates.keys()])
        expression_values = {f":{k}": v for k, v in updates.items()}

        try:
            table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values
            )
        except ClientError as e:
            print(f"Error updating item: {e}")

    # fetch record
    async def select(self, table_name: str, key: Dict[str, Any]) -> Dict[str, Any]:
        table = self.dynamodb.Table(table_name)
        try:
            response = table.get_item(Key=key)
            return response.get('Item', {})
        except ClientError as e:
            print(f"Error selecting item: {e}")
            return {}

    # delete record
    async def delete_item(self, table_name: str, key: dict):
        table = self.dynamodb.Table(table_name)

        try:
            table.delete_item(
                Key=key
            )
        except ClientError as e:
            print(f"Error deleting item: {e}")
        
    # fetch records that are begins with a secific key
    async def fetch_records_starting_with(self, table_name: str, attribute_name: str, prefix: str) -> List[Dict[str, Any]]:
        table = self.dynamodb.Table(table_name)
        try:
            response = table.scan(
                FilterExpression=Attr(attribute_name).begins_with(prefix)
            )
            return response.get('Items', [])
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
