"""Search request models."""
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class RestaurantSearchRequest(BaseModel):
    """Request model for restaurant search."""

    location: str = Field(..., description="Location string (e.g., 'New York, NY') or lat/lng coordinates")
    cuisine: Optional[str] = Field(None, description="Cuisine type filter (e.g., 'italian', 'chinese', 'mexican')")
    min_rating: Optional[float] = Field(None, ge=0.0, le=5.0, description="Minimum rating threshold (0-5)")
    min_reviews: Optional[int] = Field(None, ge=0, description="Minimum number of reviews")
    price_level: Optional[int] = Field(None, ge=0, le=4, description="Price level (0-4, where 0 is free and 4 is very expensive)")
    open_now: Optional[bool] = Field(None, description="Filter for currently open restaurants")
    radius: Optional[int] = Field(None, ge=1, le=50000, description="Search radius in meters (max 50000)")

    @field_validator("location")
    @classmethod
    def validate_location(cls, v: str) -> str:
        """Validate location is not empty."""
        if not v or not v.strip():
            raise ValueError("Location cannot be empty")
        return v.strip()

