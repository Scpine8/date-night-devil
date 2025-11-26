"""Custom exceptions for the application."""


class RestaurantSearchException(Exception):
    """Base exception for restaurant search errors."""
    pass


class GoogleMapsAPIError(RestaurantSearchException):
    """Exception raised when Google Maps API returns an error."""
    pass


class ConfigurationError(RestaurantSearchException):
    """Exception raised when configuration is invalid or missing."""
    pass


class ValidationError(RestaurantSearchException):
    """Exception raised when request validation fails."""
    pass

