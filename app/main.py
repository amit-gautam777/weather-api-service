

from fastapi import FastAPI, HTTPException, Query
from app.weather_service import fetch_weather_data, store_weather_data, retrieve_weather_data
from app.db import log_event
import uvicorn

app = FastAPI()


@app.get("/weather")
async def get_weather(city: str = Query(..., min_length=1, max_length=100)):
    try:
        cached_data = await retrieve_weather_data(city)
        if cached_data:
            return cached_data

        weather_data = await fetch_weather_data(city)

        await store_weather_data(city, weather_data)

        # await log_event(city, weather_data)

        return weather_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8009)
