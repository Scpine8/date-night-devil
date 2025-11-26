import { useCallback, useState } from "react";

// TypeScript interfaces matching the Python API models
export interface Location {
  lat: number;
  lng: number;
}

export interface Restaurant {
  place_id: string;
  name: string;
  address?: string | null;
  location?: Location | null;
  rating?: number | null;
  user_ratings_total?: number | null;
  price_level?: number | null;
  types: string[];
  opening_hours?: Record<string, unknown> | null;
  photos?: Array<Record<string, unknown>> | null;
  website?: string | null;
  phone_number?: string | null;
  business_status?: string | null;
  // Service options
  dine_in?: boolean | null;
  takeout?: boolean | null;
  delivery?: boolean | null;
  curbside_pickup?: boolean | null;
  reservable?: boolean | null;
  // Dining times
  serves_breakfast?: boolean | null;
  serves_lunch?: boolean | null;
  serves_dinner?: boolean | null;
  serves_brunch?: boolean | null;
  // Beverages
  serves_beer?: boolean | null;
  serves_wine?: boolean | null;
  serves_cocktails?: boolean | null;
  serves_coffee?: boolean | null;
  // Food types
  serves_vegetarian_food?: boolean | null;
  serves_dessert?: boolean | null;
  // Amenities
  outdoor_seating?: boolean | null;
  live_music?: boolean | null;
  good_for_children?: boolean | null;
  good_for_groups?: boolean | null;
  good_for_watching_sports?: boolean | null;
  allows_dogs?: boolean | null;
  restroom?: boolean | null;
  menu_for_children?: boolean | null;
  // Parking & payment
  parking_options?: Record<string, unknown> | null;
  payment_options?: Record<string, unknown> | null;
  // Additional info
  google_maps_uri?: string | null;
  icon_mask_base_uri?: string | null;
  utc_offset_minutes?: number | null;
  current_opening_hours?: Record<string, unknown> | null;
  regular_opening_hours?: Record<string, unknown> | null;
  generative_summary?: string | null;
  editorial_summary?: string | null;
  // Reviews
  reviews?: Array<Record<string, unknown>> | null;
  review_summary?: Record<string, unknown> | null;
  // Price & phone
  price_range?: string | null;
  international_phone_number?: string | null;
  national_phone_number?: string | null;
  // Location details
  plus_code?: Record<string, unknown> | null;
  viewport?: Record<string, unknown> | null;
  address_components?: Array<Record<string, unknown>> | null;
  adr_format_address?: string | null;
}

export interface SearchResponse {
  restaurants: Restaurant[];
  total_results: number;
  query: Record<string, unknown>;
}

export interface SearchParams {
  location: string;
  cuisine?: string;
  min_rating?: number;
  min_reviews?: number;
  price_level?: number;
  open_now?: boolean;
  radius?: number;
  country?: string;
}

export interface UsePlacesAPIReturn {
  fetchPlaces: (params: SearchParams) => Promise<SearchResponse | null>;
  loading: boolean;
  error: string | null;
  data: SearchResponse | null;
}

const DEFAULT_API_BASE_URL = "http://localhost:8000";

/**
 * Custom hook for interacting with the Date Night Devil restaurant search API.
 * Exposes fetchPlaces function and manages loading, error, and data states.
 */
export function usePlacesAPI(
  apiBaseUrl: string = DEFAULT_API_BASE_URL
): UsePlacesAPIReturn {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<SearchResponse | null>(null);

  const fetchPlaces = useCallback(
    async (params: SearchParams): Promise<SearchResponse | null> => {
      setLoading(true);
      setError(null);

      try {
        // Build query parameters
        const searchParams = new URLSearchParams();
        searchParams.append("location", params.location);

        if (params.cuisine) {
          searchParams.append("cuisine", params.cuisine);
        }
        if (params.min_rating !== undefined) {
          searchParams.append("min_rating", params.min_rating.toString());
        }
        if (params.min_reviews !== undefined) {
          searchParams.append("min_reviews", params.min_reviews.toString());
        }
        if (params.price_level !== undefined) {
          searchParams.append("price_level", params.price_level.toString());
        }
        if (params.open_now !== undefined) {
          searchParams.append("open_now", params.open_now.toString());
        }
        if (params.radius !== undefined) {
          searchParams.append("radius", params.radius.toString());
        }

        const url = `${apiBaseUrl}/restaurants/search?${searchParams.toString()}`;

        const response = await fetch(url, {
          method: "GET",
          headers: {
            Accept: "application/json",
          },
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({
            error: "Unknown error",
            detail: `HTTP ${response.status}: ${response.statusText}`,
          }));
          throw new Error(
            errorData.detail || errorData.error || "Failed to fetch restaurants"
          );
        }

        // Check if response has content before parsing
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
          throw new Error(
            `Expected JSON response but got ${
              contentType || "unknown content type"
            }`
          );
        }

        const text = await response.text();
        if (!text) {
          throw new Error("Empty response body");
        }

        const result: SearchResponse = JSON.parse(text);
        setData(result);
        return result;
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "An unexpected error occurred";
        setError(errorMessage);
        console.error("Error fetching places:", err);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [apiBaseUrl]
  );

  return {
    fetchPlaces,
    loading,
    error,
    data,
  };
}
