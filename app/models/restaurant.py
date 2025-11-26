"""Restaurant response models."""
from typing import Optional

from pydantic import BaseModel, Field


class Location(BaseModel):
    """Location coordinates."""

    lat: float
    lng: float


class Restaurant(BaseModel):
    """Restaurant model with details from Google Places API."""

    place_id: str = Field(..., description="Google Places ID")
    name: str = Field(..., description="Restaurant name")
    address: Optional[str] = Field(None, description="Formatted address")
    location: Optional[Location] = Field(None, description="Geographic coordinates")
    rating: Optional[float] = Field(None, ge=0.0, le=5.0, description="Average rating")
    user_ratings_total: Optional[int] = Field(None, ge=0, description="Total number of reviews")
    price_level: Optional[int] = Field(None, ge=0, le=4, description="Price level (0-4)")
    types: list[str] = Field(default_factory=list, description="List of place types")
    opening_hours: Optional[dict] = Field(None, description="Opening hours information")
    photos: Optional[list[dict]] = Field(None, description="Photo references")
    website: Optional[str] = Field(None, description="Restaurant website URL")
    phone_number: Optional[str] = Field(None, description="Phone number")
    business_status: Optional[str] = Field(None, description="Business status")


class SearchResponse(BaseModel):
    """Response model for restaurant search."""

    restaurants: list[Restaurant] = Field(default_factory=list, description="List of restaurants")
    total_results: int = Field(..., description="Total number of results found")
    query: dict = Field(..., description="Query parameters used for search")

