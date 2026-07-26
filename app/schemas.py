from typing import Literal

from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    unit: Literal["celsius"]
