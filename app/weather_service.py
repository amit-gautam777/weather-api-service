import aiohttp
import asyncio
import json
from datetime import datetime
from typing import Optional
from app.storage import save_to_s3, load_from_s3

API_KEY = "9cd6095f42014666969f7db496975494"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

async def fetch_weather_data(city: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params={"q": city, "appid": API_KEY}) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Error fetching weather data for {city}: {response.status}")

async def store_weather_data(city: str, data: dict) -> None:
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    filename = f"{city}_{timestamp}.json"
    await save_to_s3(filename, json.dumps(data))

async def retrieve_weather_data(city: str) -> Optional[dict]:
    # Implement cache expiration logic
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    filename = f"{city}_*.json"  # Fetch the latest file
    data = await load_from_s3(filename)
    if data:
        return json.loads(data)
    return None
