import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui/table";
import type { Restaurant } from "@/hooks/usePlacesAPI";

interface RestaurantTableProps {
	restaurants: Restaurant[];
}

export function RestaurantTable({ restaurants }: RestaurantTableProps) {
	const formatPriceLevel = (level: number | null | undefined): string => {
		if (level === null || level === undefined) return "N/A";
		return "$".repeat(level);
	};

	const formatRating = (rating: number | null | undefined): string => {
		if (rating === null || rating === undefined) return "N/A";
		return rating.toFixed(1);
	};

	if (restaurants.length === 0) {
		return (
			<div className="w-full rounded-md border p-4 text-center text-muted-foreground">
				No restaurants found
			</div>
		);
	}

	return (
		<div className="w-full overflow-x-auto rounded-md border">
			<Table>
				<TableHeader>
					<TableRow>
						<TableHead>Name</TableHead>
						<TableHead>Address</TableHead>
						<TableHead>Rating</TableHead>
						<TableHead>Reviews</TableHead>
						<TableHead>Price Level</TableHead>
						<TableHead>Phone</TableHead>
					</TableRow>
				</TableHeader>
				<TableBody>
					{restaurants.map((restaurant) => (
						<TableRow key={restaurant.place_id}>
							<TableCell className="font-medium">
								{restaurant.name}
							</TableCell>
							<TableCell>{restaurant.address || "N/A"}</TableCell>
							<TableCell>{formatRating(restaurant.rating)}</TableCell>
							<TableCell>
								{restaurant.user_ratings_total?.toLocaleString() || "N/A"}
							</TableCell>
							<TableCell>
								{formatPriceLevel(restaurant.price_level)}
							</TableCell>
							<TableCell>{restaurant.phone_number || "N/A"}</TableCell>
						</TableRow>
					))}
				</TableBody>
			</Table>
		</div>
	);
}

