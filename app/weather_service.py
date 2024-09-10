import aiohttp
import asyncio
import json
from datetime import datetime
from typing import Optional
from app.storage import save_to_s3, load_from_s3
import os
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta
import boto3


async def fetch_weather_data(city: str) -> dict:
    async with aiohttp.ClientSession() as session:
        params = {
                "q": city, 
                "appid": os.getenv("WEATHER_API_KEY")
            }

        async with session.get(os.getenv("WEATHER_BASE_URL"), params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Error fetching weather data for {city}: {response.status}")

# Store weather detail
async def store_weather_data(city: str, data: dict, dynamodb, fileClient) -> None:
    now = datetime.utcnow()

    expired_at_obj = now + timedelta(minutes=os.getenv("CACHE_EXPIRATION_MINUTES"))
    expired_at = expired_at_obj.strftime('%Y%m%d%H%M%S')
    filename = f"{city}_{expired_at}.json"

    item = {
        "expired_at": expired_at,
        "filename": filename
    }
    response = await dynamodb.create('cache', item)
    print(response)

    # await save_to_s3(filename, json.dumps(data))


# To get weather detail 
async def retrieve_weather_data(city: str, dynamodb, fileClient) -> Optional[dict]:
    response = await dynamodb.fetch_records_starting_with('cache', 'filename', f'{city}_')

    print(response)
    print(len(response))

    now = datetime.utcnow()
    five_minutes_ago = now - timedelta(minutes=os.getenv("CACHE_EXPIRATION_MINUTES"))
    five_minutes_ago_str = five_minutes_ago.strftime('%Y%m%dT%H%M%S')

    # if response:
    #     if response.expire_at > five_minutes_ago_str:
    #         fileClient.
    return response
            
