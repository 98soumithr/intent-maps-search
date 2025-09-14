from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum


class PlaceType(str, Enum):
    RESTAURANT = "restaurant"
    CAFE = "cafe"
    COFFEE_SHOP = "coffee shop"
    BAR = "bar"
    HOTEL = "hotel"
    GAS_STATION = "gas station"
    PARKING = "parking"
    PHARMACY = "pharmacy"
    HOSPITAL = "hospital"
    STORE = "store"
    OTHER = "other"


class ConstraintType(str, Enum):
    PARKING = "parking"
    QUIET = "quiet"
    OPEN_LATE = "open late"
    WIFI = "wifi"
    RATING_MIN = "rating_min"
    TIME_LIMIT = "time_limit"
    PRICE_RANGE = "price_range"


class ParsedQuery(BaseModel):
    place_type: str
    locations: List[str]
    constraints: List[Dict[str, Any]]
    midpoint_calculation: bool = False
    radius: Optional[int] = None  # in meters


class Location(BaseModel):
    lat: float
    lng: float
    address: str


class PlaceResult(BaseModel):
    name: str
    place_id: str
    address: str
    rating: Optional[float]
    price_level: Optional[int]
    opening_hours: Optional[Dict[str, Any]]
    photos: Optional[List[str]]
    distance_from_midpoint: Optional[float]  # in meters
    distance_text: Optional[str]
    types: List[str]


class SearchResponse(BaseModel):
    query: str
    parsed_query: ParsedQuery
    results: List[PlaceResult]
    midpoint: Optional[Location]
    execution_time: float
