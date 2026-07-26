import random

from fastapi import FastAPI, Query

from app.schemas import WeatherResponse

app = FastAPI(title="Dummy Weather API")


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "Dummy Weather API",
        "docs": "/docs",
        "weather": "/weather?city=<city>",
    }


@app.get("/weather", response_model=WeatherResponse)
def get_weather(city: str = Query(..., min_length=1)) -> WeatherResponse:
    temperature = round(random.uniform(-20.0, 40.0), 1)
    return WeatherResponse(city=city, temperature=temperature, unit="celsius")
