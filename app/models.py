from pydantic import BaseModel
from typing import List
from enum import Enum


class Freshness(str, Enum):
    fresh = "fresh"
    normal = "normal"
    old = "old"


class MushroomCreate(BaseModel):
    name: str
    edible: bool
    weight: float
    freshness: Freshness


class Mushroom(MushroomCreate):
    id: int


class BasketCreate(BaseModel):
    owner: str
    capacity: float


class BasketAddMushroom(BaseModel):
    mushroom_id: int


class Basket(BasketCreate):
    id: int
    mushrooms: List[Mushroom] = []
