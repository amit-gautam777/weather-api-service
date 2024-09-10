import aiohttp
from datetime import datetime
from typing import Optional
import os
from datetime import datetime, timedelta
import json


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

    expired_at_obj = now + timedelta(minutes=int(os.getenv("CACHE_EXPIRATION_MINUTES")))
    expired_at = expired_at_obj.strftime('%Y-%m-%dT%H:%M:%S')
    filename = f"{city}_{expired_at}.json"

    file_upload_response = await fileClient.upload_file_content(os.getenv('AWS_S3_CACHE_DIRECTORY'), filename, json.dumps(data), 'application/json')
    print(f'file_upload_response: ${file_upload_response}')

    if file_upload_response:
        item = {
            "expired_at": expired_at,
            "filename": filename
        }
        await dynamodb.create('cache', item)

    return


# To get weather detail 
async def retrieve_weather_data(city: str, dynamodb, fileClient) -> Optional[dict]:
    response = await dynamodb.fetch_records_starting_with('cache', 'filename', f'{city}_')

    now = datetime.utcnow()
    cache_expiration_time_obj = now - timedelta(minutes=int(os.getenv("CACHE_EXPIRATION_MINUTES")))
    cache_expiration_time = cache_expiration_time_obj.strftime('%Y-%m-%dT%H:%M:%S')

    if response:
        if response[0]['expired_at'] >= cache_expiration_time:
            file_content = await fileClient.get_file(os.getenv('AWS_S3_CACHE_DIRECTORY'), response[0]['filename'])
            if file_content:
                print(f'cache_file_content: ${file_content}')
                return json.loads(file_content)
        else:
            file_delete_response = await fileClient.delete_file(os.getenv('AWS_S3_CACHE_DIRECTORY'), response[0]['filename'])

            print(f'File deleted: {file_delete_response}')
            if file_delete_response:
                key = {
                    'filename': response[0]['filename'],
                    'expired_at': response[0]['expired_at']
                }
                await dynamodb.delete_item('cache', key)
    
    # fetch and store weather data
    data = await fetch_weather_data(city)
    await store_weather_data(city, data, dynamodb, fileClient)
    return data
