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
    user_ratings_total: Optional[int] = Field(
        None, ge=0, description="Total number of reviews"
    )
    price_level: Optional[int] = Field(
        None, ge=0, le=4, description="Price level (0-4)"
    )
    types: list[str] = Field(default_factory=list, description="List of place types")
    opening_hours: Optional[dict] = Field(None, description="Opening hours information")
    photos: Optional[list[dict]] = Field(None, description="Photo references")
    website: Optional[str] = Field(None, description="Restaurant website URL")
    phone_number: Optional[str] = Field(None, description="Phone number")
    business_status: Optional[str] = Field(None, description="Business status")
    # Service options
    dine_in: Optional[bool] = Field(None, description="Dine-in available")
    takeout: Optional[bool] = Field(None, description="Takeout available")
    delivery: Optional[bool] = Field(None, description="Delivery available")
    curbside_pickup: Optional[bool] = Field(None, description="Curbside pickup available")
    reservable: Optional[bool] = Field(None, description="Reservations accepted")
    # Dining times
    serves_breakfast: Optional[bool] = Field(None, description="Serves breakfast")
    serves_lunch: Optional[bool] = Field(None, description="Serves lunch")
    serves_dinner: Optional[bool] = Field(None, description="Serves dinner")
    serves_brunch: Optional[bool] = Field(None, description="Serves brunch")
    # Beverages
    serves_beer: Optional[bool] = Field(None, description="Serves beer")
    serves_wine: Optional[bool] = Field(None, description="Serves wine")
    serves_cocktails: Optional[bool] = Field(None, description="Serves cocktails")
    serves_coffee: Optional[bool] = Field(None, description="Serves coffee")
    # Food types
    serves_vegetarian_food: Optional[bool] = Field(None, description="Serves vegetarian food")
    serves_dessert: Optional[bool] = Field(None, description="Serves dessert")
    # Amenities
    outdoor_seating: Optional[bool] = Field(None, description="Outdoor seating available")
    live_music: Optional[bool] = Field(None, description="Live music available")
    good_for_children: Optional[bool] = Field(None, description="Good for children")
    good_for_groups: Optional[bool] = Field(None, description="Good for groups")
    good_for_watching_sports: Optional[bool] = Field(None, description="Good for watching sports")
    allows_dogs: Optional[bool] = Field(None, description="Allows dogs")
    restroom: Optional[bool] = Field(None, description="Restroom available")
    menu_for_children: Optional[bool] = Field(None, description="Menu for children available")
    # Parking & payment
    parking_options: Optional[dict] = Field(None, description="Parking options information")
    payment_options: Optional[dict] = Field(None, description="Payment options information")
    # Additional info
    google_maps_uri: Optional[str] = Field(None, description="Google Maps URI")
    icon_mask_base_uri: Optional[str] = Field(None, description="Icon mask base URI")
    utc_offset_minutes: Optional[int] = Field(None, description="UTC offset in minutes")
    current_opening_hours: Optional[dict] = Field(None, description="Current opening hours")
    regular_opening_hours: Optional[dict] = Field(None, description="Regular opening hours schedule")
    generative_summary: Optional[str] = Field(None, description="AI-generated summary")
    editorial_summary: Optional[str] = Field(None, description="Editorial summary")
    # Reviews
    reviews: Optional[list[dict]] = Field(None, description="User reviews")
    review_summary: Optional[dict] = Field(None, description="Review summary statistics")
    # Price & phone
    price_range: Optional[str] = Field(None, description="Price range (e.g., '$$$')")
    international_phone_number: Optional[str] = Field(None, description="International phone number format")
    national_phone_number: Optional[str] = Field(None, description="National phone number format")
    # Location details
    plus_code: Optional[dict] = Field(None, description="Plus code information")
    viewport: Optional[dict] = Field(None, description="Viewport bounds")
    address_components: Optional[list[dict]] = Field(None, description="Structured address components")
    adr_format_address: Optional[str] = Field(None, description="ADR format address")


class SearchResponse(BaseModel):
    """Response model for restaurant search."""

    restaurants: list[Restaurant] = Field(
        default_factory=list, description="List of restaurants"
    )
    total_results: int = Field(..., description="Total number of results found")
    query: dict = Field(..., description="Query parameters used for search")
    next_page_token: Optional[str] = Field(
        None, description="Token to fetch the next page of results"
    )
