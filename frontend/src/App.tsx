import { SearchBar } from "@/components/ui/input";
import { RestaurantTable } from "@/components/RestaurantTable";
import { useRef } from "react";
import { usePlacesAPI } from "./hooks/usePlacesAPI";

function App() {
  const searchBarRef = useRef<HTMLInputElement>(null);
  const { fetchPlaces, loading, data, error } = usePlacesAPI();

  const handleSearch = () => {
    if (!searchBarRef.current?.value) return;
    fetchPlaces({
      location: searchBarRef.current?.value || "",
    });
  };
  return (
    <div className="flex min-h-screen flex-col items-center gap-6 bg-background p-4 text-foreground">
      <h1 className="text-4xl font-bold">Date Night Devil</h1>
      <div className="w-full max-w-md">
        <SearchBar
          type="text"
          handleSearch={handleSearch}
          placeholder="Search any city!"
          ref={searchBarRef}
        />
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
