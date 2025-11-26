import * as React from "react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

export interface SearchBarProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  handleSearch: () => void;
}

const SearchBar = React.forwardRef<HTMLInputElement, SearchBarProps>(
  ({ className, type, handleSearch, ...props }, ref) => {
    return (
      <div className="flex w-full gap-2">
        <input
          type={type}
          className={cn(
            "flex h-10 flex-1 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
            className
          )}
          ref={ref}
          {...props}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleSearch();
            }
          }}
        />
        <Button onClick={handleSearch}>Search</Button>
      </div>
    );
  }
);
SearchBar.displayName = "SearchBar";

export { SearchBar };
