import boto3
from boto3.dynamodb.conditions import Key
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

    async def create(self, table_name: str, item: Dict[str, Any]) -> None:
        table = self.dynamodb.Table(table_name)
        try:
            table.put_item(Item=item)
        except ClientError as e:
            print(f"Error creating item: {e}")

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

    async def select(self, table_name: str, key: Dict[str, Any]) -> Dict[str, Any]:
        table = self.dynamodb.Table(table_name)
        try:
            response = table.get_item(Key=key)
            return response.get('Item', {})
        except ClientError as e:
            print(f"Error selecting item: {e}")
            return {}
        

    async def fetch_records_starting_with(self, table_name: str, attribute_name: str, prefix: str) -> List[Dict[str, Any]]:
        try:
            table = self.dynamodb.Table(table_name)
            response = table.scan(
                FilterExpression=Key(attribute_name).begins_with(prefix)
            )

            print("========================================")
            print(response.get('Item', {}))
            print("========================================")
            
            items = response.get('Item', {})
            return items
        
        except ClientError as e:
            print(f"Error selecting item: {e}")
            return {}
