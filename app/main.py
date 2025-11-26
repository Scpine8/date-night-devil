"""Main FastAPI application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
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


@app.exception_handler(RestaurantSearchException)
async def restaurant_search_exception_handler(request, exc: RestaurantSearchException):
    """Handle custom restaurant search exceptions."""
    if isinstance(exc, ConfigurationError):
        return JSONResponse(
            status_code=500,
            content={"error": "Configuration error", "detail": str(exc)}
        )
    elif isinstance(exc, GoogleMapsAPIError):
        return JSONResponse(
            status_code=502,
            content={"error": "Google Maps API error", "detail": str(exc)}
        )
    elif isinstance(exc, ValidationError):
        return JSONResponse(
            status_code=400,
            content={"error": "Validation error", "detail": str(exc)}
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(exc)}
        )


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint."""
    return {
        "message": "Restaurant Search API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "google_maps_configured": settings.is_google_maps_configured
    }


@app.get(
    "/restaurants/search",
    response_model=SearchResponse,
    tags=["Restaurants"],
    summary="Search restaurants with advanced filters",
    description="Search for restaurants in a given location with filters for cuisine, rating, reviews, price level, and open status."
)
async def search_restaurants(
    location: str = Query(..., description="Location string (e.g., 'New York, NY') or lat/lng coordinates"),
    cuisine: str | None = Query(None, description="Cuisine type filter (e.g., 'italian', 'chinese', 'mexican')"),
    min_rating: float | None = Query(None, ge=0.0, le=5.0, description="Minimum rating threshold (0-5)"),
    min_reviews: int | None = Query(None, ge=0, description="Minimum number of reviews"),
    price_level: int | None = Query(None, ge=0, le=4, description="Price level (0-4, where 0 is free and 4 is very expensive)"),
    open_now: bool | None = Query(None, description="Filter for currently open restaurants"),
    radius: int | None = Query(None, ge=1, le=50000, description="Search radius in meters (max 50000)"),
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
    """
    if not google_maps_service:
        raise HTTPException(
            status_code=500,
            detail="Google Maps API is not configured. Please set GOOGLE_MAPS_API_KEY environment variable."
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
        )
        
        return SearchResponse(
            restaurants=restaurants,
            total_results=len(restaurants),
            query=search_request.model_dump(exclude_none=True)
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

