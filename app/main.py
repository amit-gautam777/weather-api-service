from fastapi import FastAPI, Depends, HTTPException, Query
from dotenv import load_dotenv
from app.weather_service import retrieve_weather_data
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI()


from app.service.database.dynamo import DynamoDBClient
from app.service.storage.S3Storage import S3Storage

# Dependencies
async def get_dynamodb_client() -> DynamoDBClient:
    return DynamoDBClient()

def get_s3_client() -> S3Storage:
    return S3Storage()


@app.get("/weather")
async def get_weather(city: str = Query(..., min_length=1, max_length=100), db: DynamoDBClient = Depends(get_dynamodb_client), fileClient: S3Storage = Depends(get_s3_client)):
    try:
        return await retrieve_weather_data(city, db, fileClient)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=80)
