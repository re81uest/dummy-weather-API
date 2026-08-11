import random
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
from prometheus_fastapi_instrumentator import Instrumentator

from app.database import init_db
from app.middleware import RequestResponseLoggingMiddleware
from app.schemas import WeatherResponse


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Dummy Weather API", lifespan=lifespan)
app.add_middleware(RequestResponseLoggingMiddleware)
Instrumentator().instrument(app).expose(app)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "Dummy Weather API",
        "docs": "/docs",
        "weather": "/weather?city=<city>",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/weather", response_model=WeatherResponse)
def get_weather(city: str = Query(..., min_length=1)) -> WeatherResponse:
    temperature = round(random.uniform(-20.0, 40.0), 1)
    return WeatherResponse(city=city, temperature=temperature, unit="celsius")
