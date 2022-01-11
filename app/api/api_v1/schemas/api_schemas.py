import datetime as dt
from pydantic import BaseModel
from typing import List, Optional


class PredictorVariables(BaseModel):
    house_surface: int
    garden_surface: int
    rooms: int


class PriceRange(BaseModel):
    lower_price: Optional[float]
    upper_price: Optional[float]


class HousePrice(BaseModel):
    price_in_euros: float


class HouseVariablesAdd(PredictorVariables):
    link: str
    city: str
    price: int


class HouseVariablesReturn(HouseVariablesAdd):
    time_added: dt.datetime


class HouseDataReturn(BaseModel):
    data: List[HouseVariablesReturn]


class AuthDetails(BaseModel):
    username: str
    password: str
