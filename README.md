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

### Using Make (Recommended)

The project includes a Makefile with convenient aliases:

```bash
make start    # Start the development server with auto-reload
make install  # Install dependencies
make setup    # Install dependencies and setup project
make clean    # Clean Python cache files
make help     # Show all available commands
```

Simply run:

```bash
make start
```

### Alternative: Direct Commands

Start the development server directly:

```bash
uvicorn app.main:app --reload
```

Or run directly:

```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Interactive API docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative docs**: http://localhost:8000/redoc (ReDoc)

## API Endpoints

### GET /restaurants/search

Search for restaurants with advanced filtering options.

#### Query Parameters

| Parameter     | Type    | Required | Description                                                                      |
| ------------- | ------- | -------- | -------------------------------------------------------------------------------- |
| `location`    | string  | Yes      | Location string (e.g., "New York, NY") or coordinates (e.g., "40.7128,-74.0060") |
| `cuisine`     | string  | No       | Cuisine type filter (e.g., "italian", "chinese", "mexican")                      |
| `min_rating`  | float   | No       | Minimum rating threshold (0-5)                                                   |
| `min_reviews` | integer | No       | Minimum number of reviews                                                        |
| `price_level` | integer | No       | Price level (0-4, where 0 is free and 4 is very expensive)                       |
| `open_now`    | boolean | No       | Filter for currently open restaurants                                            |
| `radius`      | integer | No       | Search radius in meters (max 50000)                                              |

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
        "lng": -74.006
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
3. **Enable Billing**: You must enable billing on your Google Cloud project, even for the free tier. Go to [Billing Settings](https://console.cloud.google.com/project/_/billing/enable) and enable billing for your project.
4. Enable the **Places API** (and **Places API (New)** if available)
   - Navigate to "APIs & Services" > "Library"
   - Search for "Places API" and enable it
   - Also enable "Places API (New)" if you want to use the new version
5. Create credentials (API Key)
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
6. Restrict the API key to Places API for security
   - Click on your API key to edit it
   - Under "API restrictions", select "Restrict key" and choose "Places API"
   - **Important**: If you restrict by IP or HTTP referrer, make sure your server's IP address or domain is included
7. Add the API key to your `.env` file:
   ```bash
   GOOGLE_MAPS_API_KEY=your_api_key_here
   ```

**Important**: Google requires billing to be enabled even if you're using the free tier ($200 monthly credit). Without billing enabled, you'll receive a `REQUEST_DENIED` error.

## Troubleshooting

### REQUEST_DENIED Error

If you're getting a `REQUEST_DENIED` error even though billing is enabled, check the following:

1. **Verify Places API is Enabled**

   - Go to [APIs & Services > Library](https://console.cloud.google.com/apis/library)
   - Search for "Places API" and ensure it's enabled
   - Also check "Places API (New)" if available

2. **Check API Key Restrictions**

   - Go to [APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
   - Click on your API key
   - Under "API restrictions":
     - If "Don't restrict key" is selected, try restricting to "Places API" only
     - If restricted, ensure "Places API" is in the allowed list
   - Under "Application restrictions":
     - If "None" is selected, that's fine
     - If "IP addresses" is selected, ensure your server's IP is included
     - If "HTTP referrers" is selected, ensure your domain is included (not needed for server-side API calls)

3. **Verify API Key is Correct**

   - Ensure the API key in your `.env` file matches the one in Google Cloud Console
   - Check for any extra spaces or newlines in the `.env` file
   - Verify the API key hasn't been deleted or regenerated

4. **Check API Quotas**

   - Go to [APIs & Services > Dashboard](https://console.cloud.google.com/apis/dashboard)
   - Check if you've exceeded any quotas or limits
   - Review the "Quotas" tab for Places API

5. **Verify Project and Billing**

   - Ensure the API key belongs to the project with billing enabled
   - Check that billing account is active: [Billing Settings](https://console.cloud.google.com/billing)

6. **Use Debug Endpoint**

   - Start your server and visit: `http://localhost:8000/debug/google-maps`
   - This will show detailed information about the API configuration and test a sample request
   - Review the `full_response` field for detailed error information

7. **Check Error Details**
   - The API response may include `error_details` array with specific reasons
   - Common issues:
     - API not enabled
     - API key restrictions too strict
     - Billing not enabled (even if you think it is)
     - Wrong project selected

### Common Issues

- **"API key not valid"**: API key may be incorrect, deleted, or belongs to a different project
- **"This API project is not authorized to use this API"**: Places API is not enabled for the project
- **"Requests from referer are not allowed"**: IP/HTTP referrer restrictions are blocking your request
- **"Billing has not been enabled"**: Billing account needs to be linked to the project

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
