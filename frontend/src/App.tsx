import { SearchBar } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { RestaurantTable } from "@/components/RestaurantTable";
import { useRef, useState } from "react";
import { usePlacesAPI } from "./hooks/usePlacesAPI";
import { cn } from "@/lib/utils";

function App() {
  const searchBarRef = useRef<HTMLInputElement>(null);
  const { fetchPlaces, loading, data, error } = usePlacesAPI();

  const [cuisine, setCuisine] = useState<string>("");
  const [minRating, setMinRating] = useState<string>("");
  const [minReviews, setMinReviews] = useState<string>("");
  const [priceLevel, setPriceLevel] = useState<string>("");

  const handleSearch = () => {
    if (!searchBarRef.current?.value) return;

    const searchParams: {
      location: string;
      cuisine?: string;
      min_rating?: number;
      min_reviews?: number;
      price_level?: number;
    } = {
      location: searchBarRef.current?.value || "",
    };

    if (cuisine.trim()) {
      searchParams.cuisine = cuisine.trim();
    }
    if (minRating.trim()) {
      const rating = parseFloat(minRating);
      if (!isNaN(rating) && rating >= 0 && rating <= 5) {
        searchParams.min_rating = rating;
      }
    }
    if (minReviews.trim()) {
      const reviews = parseInt(minReviews, 10);
      if (!isNaN(reviews) && reviews >= 0) {
        searchParams.min_reviews = reviews;
      }
    }
    if (priceLevel && priceLevel !== "") {
      const price = parseInt(priceLevel, 10);
      if (!isNaN(price)) {
        searchParams.price_level = price;
      }
    }

    fetchPlaces(searchParams);
  };
  return (
    <div className="flex min-h-screen flex-col items-center gap-6 bg-background p-4 text-foreground">
      <h1 className="text-4xl font-bold">Date Night Devil</h1>
      <div className="w-full max-w-4xl">
        <div className="mb-4 flex w-full flex-wrap gap-3">
          <input
            type="text"
            placeholder="Cuisine (e.g., italian)"
            value={cuisine}
            onChange={(e) => setCuisine(e.target.value)}
            className={cn(
              "flex h-10 w-40 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            )}
          />
          <input
            type="number"
            placeholder="Min Rating (0-5)"
            value={minRating}
            onChange={(e) => setMinRating(e.target.value)}
            min="0"
            max="5"
            step="0.1"
            className={cn(
              "flex h-10 w-32 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            )}
          />
          <input
            type="number"
            placeholder="Min Reviews"
            value={minReviews}
            onChange={(e) => setMinReviews(e.target.value)}
            min="0"
            className={cn(
              "flex h-10 w-32 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            )}
          />
          <Select
            value={priceLevel}
            onChange={(e) => setPriceLevel(e.target.value)}
            className="h-10 w-32"
          >
            <option value="">Any</option>
            <option value="1">$</option>
            <option value="2">$$</option>
            <option value="3">$$$</option>
            <option value="4">$$$$</option>
          </Select>
          <div className="flex-1 min-w-[200px]">
            <SearchBar
              type="text"
              handleSearch={handleSearch}
              placeholder="Search any city!"
              ref={searchBarRef}
            />
          </div>
        </div>
      </div>

      {loading && (
        <div className="w-full max-w-6xl">
          <p className="text-center text-muted-foreground">Loading...</p>
        </div>
      )}

      {error && (
        <div className="w-full max-w-6xl rounded-md border border-destructive bg-destructive/10 p-4">
          <p className="text-center text-destructive">Error: {error}</p>
        </div>
      )}

      {data && !loading && (
        <div className="w-full max-w-6xl">
          <div className="mb-4 text-center">
            <p className="text-lg font-semibold">
              Found {data.total_results} restaurant
              {data.total_results !== 1 ? "s" : ""}
            </p>
          </div>
          <RestaurantTable restaurants={data.restaurants} />
        </div>
      )}
    </div>
  );
}

export default App;
