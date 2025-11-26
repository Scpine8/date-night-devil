"""Configuration management for the application."""
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Google Maps API Configuration
    google_maps_api_key: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    
    # Server Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # Google Maps API Base URL
    google_maps_api_base_url: str = "https://maps.googleapis.com/maps/api/place"
    
    @property
    def is_google_maps_configured(self) -> bool:
        """Check if Google Maps API key is configured."""
        return bool(self.google_maps_api_key)


settings = Settings()

