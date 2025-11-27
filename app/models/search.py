"""Search request models."""

from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class RestaurantSearchRequest(BaseModel):
    """Request model for restaurant search."""

    location: Optional[str] = Field(
        None, description="Location string (e.g., 'New York, NY') or lat/lng coordinates"
    )
    cuisine: Optional[str] = Field(
        None, description="Cuisine type filter (e.g., 'italian', 'chinese', 'mexican')"
    )
    min_rating: Optional[float] = Field(
        None, ge=0.0, le=5.0, description="Minimum rating threshold (0-5)"
    )
    min_reviews: Optional[int] = Field(
        None, ge=0, description="Minimum number of reviews"
    )
    price_level: Optional[int] = Field(
        None,
        ge=0,
        le=4,
        description="Price level (0-4, where 0 is free and 4 is very expensive)",
    )
    open_now: Optional[bool] = Field(
        None, description="Filter for currently open restaurants"
    )
    radius: Optional[int] = Field(
        None, ge=1, le=50000, description="Search radius in meters (max 50000)"
    )
    country: Optional[str] = Field(
        None,
        description="ISO 3166-1 Alpha-2 country code (e.g., 'us', 'uk', 'fr') to bias search results",
        min_length=2,
        max_length=2,
    )
    page_token: Optional[str] = Field(
        None, description="Token to fetch the next page of results from Google Places API"
    )

    @field_validator("location")
    @classmethod
    def validate_location(cls, v: Optional[str]) -> Optional[str]:
        """Validate location is not empty if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError("Location cannot be empty")
        return v.strip() if v else None

    @field_validator("country")
    @classmethod
    def validate_country(cls, v: Optional[str]) -> Optional[str]:
        """Validate country code is lowercase if provided."""
        if v:
            return v.lower()
        return v

    @model_validator(mode="after")
    def validate_location_or_page_token(self):
        """Validate that either location or page_token is provided."""
        if not self.location and not self.page_token:
            raise ValueError("Either 'location' or 'page_token' must be provided")
        return self
