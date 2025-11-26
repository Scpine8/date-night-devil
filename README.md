# Restaurant Search API Service

A fast Python API service built with FastAPI that connects to Google Maps Places API to provide advanced restaurant search capabilities with filtering by cuisine type, review ratings, number of reviews, price level, and more.

## Features

- **Advanced Restaurant Search**: Search restaurants by location with multiple filter options
- **Cuisine Filtering**: Filter by specific cuisine types (e.g., Italian, Chinese, Mexican)
- **Rating Filters**: Filter by minimum rating threshold
- **Review Count Filters**: Filter by minimum number of reviews
- **Price Level Filtering**: Filter by price level (0-4 scale)
- **Open Now Filter**: Filter for restaurants currently open
- **Radius Search**: Specify search radius in meters
- **Fast Performance**: Built with FastAPI for async/await support
- **Type Safety**: Full Pydantic validation for requests and responses

## Prerequisites

- Python 3.9 or higher
- Google Maps API key with Places API enabled
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd date-night-devil
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env` (if available) or create a `.env` file
   - Add your Google Maps API key:
```bash
GOOGLE_MAPS_API_KEY=your_api_key_here
```

## Running the Service

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Alternative: Run directly
```bash
python -m app.main
```

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative docs**: http://localhost:8000/redoc (ReDoc)

## API Endpoints

### GET /restaurants/search

Search for restaurants with advanced filtering options.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `location` | string | Yes | Location string (e.g., "New York, NY") or coordinates (e.g., "40.7128,-74.0060") |
| `cuisine` | string | No | Cuisine type filter (e.g., "italian", "chinese", "mexican") |
| `min_rating` | float | No | Minimum rating threshold (0-5) |
| `min_reviews` | integer | No | Minimum number of reviews |
| `price_level` | integer | No | Price level (0-4, where 0 is free and 4 is very expensive) |
| `open_now` | boolean | No | Filter for currently open restaurants |
| `radius` | integer | No | Search radius in meters (max 50000) |

#### Example Requests

**Basic search:**
```bash
curl "http://localhost:8000/restaurants/search?location=New%20York,%20NY"
```

**Search with filters:**
```bash
curl "http://localhost:8000/restaurants/search?location=San%20Francisco&cuisine=italian&min_rating=4.0&min_reviews=50&price_level=2&open_now=true&radius=5000"
```

**Search by coordinates:**
```bash
curl "http://localhost:8000/restaurants/search?location=40.7128,-74.0060&cuisine=mexican&min_rating=4.5"
```

#### Example Response

```json
{
  "restaurants": [
    {
      "place_id": "ChIJ...",
      "name": "Example Restaurant",
      "address": "123 Main St, New York, NY 10001",
      "location": {
        "lat": 40.7128,
        "lng": -74.0060
      },
      "rating": 4.5,
      "user_ratings_total": 250,
      "price_level": 2,
      "types": ["restaurant", "food", "point_of_interest"],
      "opening_hours": {
        "open_now": true
      },
      "website": "https://example.com",
      "phone_number": "+1 212-555-1234",
      "business_status": "OPERATIONAL"
    }
  ],
  "total_results": 1,
  "query": {
    "location": "New York, NY",
    "cuisine": "italian",
    "min_rating": 4.0,
    "min_reviews": 50
  }
}
```

### GET /health

Health check endpoint to verify service status and configuration.

**Response:**
```json
{
  "status": "healthy",
  "google_maps_configured": true
}
```

### GET /

Root endpoint with service information.

**Response:**
```json
{
  "message": "Restaurant Search API",
  "version": "1.0.0",
  "status": "running"
}
```

## Project Structure

```
date-night-devil/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app and routes
│   ├── config.py            # Configuration management
│   ├── exceptions.py        # Custom exceptions
│   ├── models/
│   │   ├── __init__.py
│   │   ├── restaurant.py    # Restaurant response models
│   │   └── search.py        # Search request models
│   └── services/
│       ├── __init__.py
│       └── google_maps.py   # Google Maps API client
├── .gitignore
├── requirements.txt
└── README.md
```

## Error Handling

The API uses custom exceptions for better error handling:

- **400 Bad Request**: Validation errors (invalid parameters)
- **500 Internal Server Error**: Configuration errors or unexpected errors
- **502 Bad Gateway**: Google Maps API errors

Example error response:
```json
{
  "error": "Google Maps API error",
  "detail": "API error message here"
}
```

## Google Maps API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Places API** (and **Places API (New)** if available)
4. Create credentials (API Key)
5. Restrict the API key to Places API for security
6. Add the API key to your `.env` file

## Notes

- Restaurant age filtering is limited by Google Maps API data availability
- The service uses Google Places API Text Search for flexible location queries
- API keys should be stored in environment variables and never committed to git
- Consider implementing rate limiting for production use
- The service queries Google Maps APIs directly without caching (as per POC requirements)

## Development

### Running Tests

(Add test instructions when tests are implemented)

### Code Quality

The project uses:
- **FastAPI** for async web framework
- **Pydantic** for data validation
- **httpx** for async HTTP client
- **python-dotenv** for environment management

## License

(Add license information)

