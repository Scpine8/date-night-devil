"""Google Maps Places API service."""

import httpx
from typing import Optional

from app.config import settings
from app.exceptions import GoogleMapsAPIError, ConfigurationError
from app.models.restaurant import Restaurant, Location


class GoogleMapsService:
    """Service for interacting with Google Maps Places API."""

    def __init__(self):
        """Initialize the Google Maps service."""
        if not settings.is_google_maps_configured:
            raise ConfigurationError("GOOGLE_MAPS_API_KEY is not configured")

        self.api_key = settings.google_maps_api_key
        self.base_url = settings.google_maps_api_base_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def search_restaurants(
        self,
        location: str,
        cuisine: Optional[str] = None,
        min_rating: Optional[float] = None,
        min_reviews: Optional[int] = None,
        price_level: Optional[int] = None,
        open_now: Optional[bool] = None,
        radius: Optional[int] = None,
    ) -> list[Restaurant]:
        """
        Search for restaurants using Google Places API Text Search.

        Args:
            location: Location string or coordinates
            cuisine: Optional cuisine type filter
            min_rating: Optional minimum rating filter
            min_reviews: Optional minimum number of reviews filter
            price_level: Optional price level filter (0-4)
            open_now: Optional filter for currently open restaurants
            radius: Optional search radius in meters

        Returns:
            List of Restaurant objects matching the criteria
        """
        # Build the query string
        query_parts = ["restaurant"]
        if cuisine:
            query_parts.append(cuisine)
        query_parts.append(f"in {location}")
        query = " ".join(query_parts)

        # Prepare API request parameters
        params = {
            "query": query,
            "key": self.api_key,
            "type": "restaurant",
        }

        if radius:
            params["radius"] = radius

        if open_now:
            params["opennow"] = "true"

        try:
            # Make the API call
            response = await self.client.get(
                f"{self.base_url}/textsearch/json", params=params
            )
            response.raise_for_status()

            data = response.json()

            # Check for API errors
            if data.get("status") != "OK" and data.get("status") != "ZERO_RESULTS":
                error_message = data.get(
                    "error_message", "Unknown Google Maps API error"
                )
                status = data.get("status", "UNKNOWN")
                error_details = data.get("error_details", [])

                # Build detailed error message
                error_info = f"Status: {status}\nError Message: {error_message}"

                # Add error details if available
                if error_details:
                    error_info += f"\nError Details: {error_details}"

                # Provide helpful message for REQUEST_DENIED errors
                if status == "REQUEST_DENIED":
                    troubleshooting = "\n\nTroubleshooting steps:\n"
                    troubleshooting += "1. Verify billing is enabled: https://console.cloud.google.com/project/_/billing/enable\n"
                    troubleshooting += "2. Check that Places API is enabled: https://console.cloud.google.com/apis/library/places-backend.googleapis.com\n"
                    troubleshooting += (
                        "3. Verify your API key is valid and not expired\n"
                    )
                    troubleshooting += "4. Check API key restrictions:\n"
                    troubleshooting += (
                        "   - If restricted by API, ensure 'Places API' is included\n"
                    )
                    troubleshooting += "   - If restricted by IP/HTTP referrer, ensure your server IP/domain is allowed\n"
                    troubleshooting += (
                        "5. Verify the API key belongs to the correct project\n"
                    )
                    troubleshooting += "6. Check API quotas haven't been exceeded\n"
                    troubleshooting += "\nFull API response: " + str(data)

                    raise GoogleMapsAPIError(
                        f"Google Maps API error: {status}\n{error_info}{troubleshooting}"
                    )

                raise GoogleMapsAPIError(
                    f"Google Maps API error: {status} - {error_info}"
                )

            # Parse results
            restaurants = []
            if "results" in data:
                for place in data["results"]:
                    restaurant = self._parse_place_result(place)

                    # Apply filters
                    if self._matches_filters(
                        restaurant,
                        min_rating=min_rating,
                        min_reviews=min_reviews,
                        price_level=price_level,
                    ):
                        restaurants.append(restaurant)

            # If we need more details (like opening hours), fetch place details
            if restaurants and open_now:
                restaurants = await self._filter_open_now(restaurants)

            return restaurants

        except httpx.HTTPStatusError as e:
            raise GoogleMapsAPIError(f"HTTP error calling Google Maps API: {e}")
        except httpx.RequestError as e:
            raise GoogleMapsAPIError(f"Request error calling Google Maps API: {e}")

    def _parse_place_result(self, place_data: dict) -> Restaurant:
        """Parse a place result from Google Places API into a Restaurant model."""
        geometry = place_data.get("geometry", {})
        location_data = geometry.get("location", {})

        location = None
        if location_data.get("lat") and location_data.get("lng"):
            location = Location(lat=location_data["lat"], lng=location_data["lng"])

        return Restaurant(
            place_id=place_data.get("place_id", ""),
            name=place_data.get("name", ""),
            address=place_data.get("formatted_address"),
            location=location,
            rating=place_data.get("rating"),
            user_ratings_total=place_data.get("user_ratings_total"),
            price_level=place_data.get("price_level"),
            types=place_data.get("types", []),
            photos=place_data.get("photos"),
            business_status=place_data.get("business_status"),
            opening_hours=place_data.get("opening_hours"),
            website=place_data.get("website"),
            phone_number=place_data.get("formatted_phone_number"),
        )

    def _matches_filters(
        self,
        restaurant: Restaurant,
        min_rating: Optional[float] = None,
        min_reviews: Optional[int] = None,
        price_level: Optional[int] = None,
    ) -> bool:
        """Check if a restaurant matches the specified filters."""
        if min_rating is not None:
            if restaurant.rating is None or restaurant.rating < min_rating:
                return False

        if min_reviews is not None:
            if (
                restaurant.user_ratings_total is None
                or restaurant.user_ratings_total < min_reviews
            ):
                return False

        if price_level is not None:
            if restaurant.price_level is None or restaurant.price_level != price_level:
                return False

        return True

    async def _filter_open_now(self, restaurants: list[Restaurant]) -> list[Restaurant]:
        """Filter restaurants to only include those currently open."""
        open_restaurants = []

        for restaurant in restaurants:
            try:
                # Fetch place details to get opening hours
                details = await self._get_place_details(restaurant.place_id)
                if details and self._is_open_now(details):
                    # Update restaurant with additional details
                    restaurant.opening_hours = details.get("opening_hours", {})
                    restaurant.website = details.get("website")
                    restaurant.phone_number = details.get("formatted_phone_number")
                    open_restaurants.append(restaurant)
            except Exception:
                # If we can't determine if it's open, skip it
                continue

        return open_restaurants

    async def _get_place_details(self, place_id: str) -> Optional[dict]:
        """Get detailed information about a place."""
        params = {
            "place_id": place_id,
            "key": self.api_key,
            "fields": "opening_hours,website,formatted_phone_number",
        }

        try:
            response = await self.client.get(
                f"{self.base_url}/details/json", params=params
            )
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "OK" and "result" in data:
                return data["result"]
        except Exception:
            pass

        return None

    def _is_open_now(self, place_details: dict) -> bool:
        """Check if a place is currently open based on opening hours."""
        opening_hours = place_details.get("opening_hours", {})
        return opening_hours.get("open_now", False)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
