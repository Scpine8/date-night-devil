"""Main FastAPI application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.exceptions import (
    RestaurantSearchException,
    GoogleMapsAPIError,
    ConfigurationError,
    ValidationError,
)
from app.models.restaurant import SearchResponse
from app.models.search import RestaurantSearchRequest
from app.services.google_maps import GoogleMapsService

# Global service instance
google_maps_service: GoogleMapsService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    global google_maps_service

    # Startup
    try:
        google_maps_service = GoogleMapsService()
    except ConfigurationError as e:
        print(f"Warning: {e}")
        google_maps_service = None

    yield

    # Shutdown
    if google_maps_service:
        await google_maps_service.close()


app = FastAPI(
    title="Restaurant Search API",
    description="Fast API service for advanced restaurant search using Google Maps",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RestaurantSearchException)
async def restaurant_search_exception_handler(request, exc: RestaurantSearchException):
    """Handle custom restaurant search exceptions."""
    if isinstance(exc, ConfigurationError):
        return JSONResponse(
            status_code=500,
            content={"error": "Configuration error", "detail": str(exc)},
        )
    elif isinstance(exc, GoogleMapsAPIError):
        return JSONResponse(
            status_code=502,
            content={"error": "Google Maps API error", "detail": str(exc)},
        )
    elif isinstance(exc, ValidationError):
        return JSONResponse(
            status_code=400, content={"error": "Validation error", "detail": str(exc)}
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(exc)},
        )


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint."""
    return {"message": "Restaurant Search API", "version": "1.0.0", "status": "running"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "google_maps_configured": settings.is_google_maps_configured,
    }


@app.get("/debug/google-maps", tags=["Debug"])
async def debug_google_maps():
    """Debug endpoint to test Google Maps API configuration."""
    if not google_maps_service:
        return {
            "error": "Google Maps service not initialized",
            "api_key_configured": settings.is_google_maps_configured,
            "api_key_length": len(settings.google_maps_api_key)
            if settings.google_maps_api_key
            else 0,
        }

    # Try a simple test query
    try:
        import httpx

        test_params = {
            "query": "restaurant in New York",
            "key": settings.google_maps_api_key,
            "type": "restaurant",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{settings.google_maps_api_base_url}/textsearch/json",
                params=test_params,
            )
            response.raise_for_status()
            data = response.json()

            result = {
                "status": "success" if data.get("status") == "OK" else "error",
                "api_response_status": data.get("status"),
                "error_message": data.get("error_message"),
                "error_details": data.get("error_details"),
                "api_key_configured": True,
                "api_key_length": len(settings.google_maps_api_key),
                "api_key_prefix": settings.google_maps_api_key[:10] + "..."
                if len(settings.google_maps_api_key) > 10
                else "N/A",
                "full_response": data,
            }

            # Add troubleshooting guidance for REQUEST_DENIED billing errors
            if (
                data.get("status") == "REQUEST_DENIED"
                and "billing" in data.get("error_message", "").lower()
            ):
                result["troubleshooting"] = {
                    "most_likely_cause": "API key belongs to a different project than the one with billing enabled",
                    "steps": [
                        "1. Go to https://console.cloud.google.com/apis/credentials",
                        "2. Click on your API key (the name, not the key value)",
                        "3. Note which Project this API key belongs to",
                        "4. Go to https://console.cloud.google.com/billing",
                        "5. Verify that SAME project has billing enabled",
                        "6. If billing is on a different project, either:",
                        "   - Enable billing on the API key's project, OR",
                        "   - Create a new API key in the project with billing enabled",
                    ],
                    "see_also": "Check TROUBLESHOOTING_BILLING.md for detailed steps",
                }

            return result
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "api_key_configured": settings.is_google_maps_configured,
            "api_key_length": len(settings.google_maps_api_key)
            if settings.google_maps_api_key
            else 0,
        }


@app.get(
    "/restaurants/search",
    response_model=SearchResponse,
    tags=["Restaurants"],
    summary="Search restaurants with advanced filters",
    description="Search for restaurants in a given location with filters for cuisine, rating, reviews, price level, and open status.",
)
async def search_restaurants(
    location: str = Query(
        ..., description="Location string (e.g., 'New York, NY') or lat/lng coordinates"
    ),
    cuisine: str | None = Query(
        None, description="Cuisine type filter (e.g., 'italian', 'chinese', 'mexican')"
    ),
    min_rating: float | None = Query(
        None, ge=0.0, le=5.0, description="Minimum rating threshold (0-5)"
    ),
    min_reviews: int | None = Query(
        None, ge=0, description="Minimum number of reviews"
    ),
    price_level: int | None = Query(
        None,
        ge=0,
        le=4,
        description="Price level (0-4, where 0 is free and 4 is very expensive)",
    ),
    open_now: bool | None = Query(
        None, description="Filter for currently open restaurants"
    ),
    radius: int | None = Query(
        None, ge=1, le=50000, description="Search radius in meters (max 50000)"
    ),
    country: str | None = Query(
        None,
        description="ISO 3166-1 Alpha-2 country code (e.g., 'us', 'uk', 'fr') to bias search results",
        min_length=2,
        max_length=2,
    ),
):
    """
    Search for restaurants with advanced filtering options.

    - **location**: Required. Location string or coordinates (e.g., "New York, NY" or "40.7128,-74.0060")
    - **cuisine**: Optional. Filter by cuisine type
    - **min_rating**: Optional. Minimum average rating (0-5)
    - **min_reviews**: Optional. Minimum number of reviews
    - **price_level**: Optional. Price level filter (0-4)
    - **open_now**: Optional. Only return restaurants currently open
    - **radius**: Optional. Search radius in meters (max 50000)
    - **country**: Optional. ISO 3166-1 Alpha-2 country code to bias search results
    """
    if not google_maps_service:
        raise HTTPException(
            status_code=500,
            detail="Google Maps API is not configured. Please set GOOGLE_MAPS_API_KEY environment variable.",
        )

    try:
        # Validate request
        search_request = RestaurantSearchRequest(
            location=location,
            cuisine=cuisine,
            min_rating=min_rating,
            min_reviews=min_reviews,
            price_level=price_level,
            open_now=open_now,
            radius=radius,
            country=country,
        )

        # Perform search
        restaurants = await google_maps_service.search_restaurants(
            location=search_request.location,
            cuisine=search_request.cuisine,
            min_rating=search_request.min_rating,
            min_reviews=search_request.min_reviews,
            price_level=search_request.price_level,
            open_now=search_request.open_now,
            radius=search_request.radius,
            country=search_request.country,
        )

        return SearchResponse(
            restaurants=restaurants,
            total_results=len(restaurants),
            query=search_request.model_dump(exclude_none=True),
        )

    except ValueError as e:
        raise ValidationError(str(e))
    except RestaurantSearchException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port)
