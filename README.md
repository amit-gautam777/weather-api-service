# Weather API Service

## Overview

This project implements a weather API service using FastAPI. The service fetches weather data asynchronously from OpenWeatherMap, caches it in AWS S3, create cache record in AWS DynamoDB, and includes Docker deployment.

## Setup

1. **Change file env.example to .env**
2. **Install docker compose on your system**:
3. **RUN docker compose to start the project**:

  ```
  docker compose --env-file ./app/.env up -d --build
  ```

4. **Run Curl Command**

```
curl -X GET "http://localhost:8002/weather?city=Chandigarh"
```