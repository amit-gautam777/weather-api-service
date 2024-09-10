from fastapi import FastAPI, Depends, HTTPException, Query
from dotenv import load_dotenv
from app.weather_service import fetch_weather_data, store_weather_data, retrieve_weather_data
from app.db import log_event
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI()


from app.service.database.dynamo import DynamoDBClient
from app.service.storage.S3Storage import S3Storage

# Dependency
def get_dynamodb_client() -> DynamoDBClient:
    return DynamoDBClient()

def get_s3_client() -> S3Storage:
    return S3Storage()



@app.get("/weather")
async def get_weather(city: str = Query(..., min_length=1, max_length=100), db: DynamoDBClient = Depends(get_dynamodb_client), fileClient: S3Storage = Depends(get_s3_client)):
    try:
        cached_data = await retrieve_weather_data(city, db, fileClient)
        if cached_data:
            return cached_data

        weather_data = await fetch_weather_data(city)
        await store_weather_data(city, weather_data, db, fileClient)

        # await log_event(city, weather_data)

        return weather_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=80)
