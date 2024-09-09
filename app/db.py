import boto3
from aiobotocore.session import get_session
from datetime import datetime
from typing import Dict

TABLE_NAME = "WeatherLog"

async def log_event(city: str, data: Dict) -> None:
    timestamp = datetime.utcnow().isoformat()
    event = {
        "city": city,
        "timestamp": timestamp,
        "data": data
    }
    session = get_session()
    async with session.create_client('dynamodb') as dynamodb:
        await dynamodb.put_item(TableName=TABLE_NAME, Item={
            "city": {"S": city},
            "timestamp": {"S": timestamp},
            "data": {"S": str(data)}
        })
