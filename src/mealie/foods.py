import logging
from typing import Any, Dict, List, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class FoodsMixin:
    """Mixin class for food-related API endpoints"""

    def get_foods(
        self,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        order_by: Optional[str] = None,
        order_direction: Optional[str] = None,
        search: Optional[str] = None,
        query_filter: Optional[str] = None,
        order_by_null_position: Optional[str] = None,
        pagination_seed: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get all foods.

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            order_by: Field to order results by
            order_direction: Direction to order results ('asc' or 'desc')
            search: Search term to filter foods
            query_filter: Advanced query filter
            order_by_null_position: How to handle nulls in ordering ('first' or 'last')
            pagination_seed: Seed for consistent pagination

        Returns:
            JSON response containing food items and pagination information
        """
        param_dict = {
            "page": page,
            "perPage": per_page,
            "orderBy": order_by,
            "orderDirection": order_direction,
            "search": search,
            "queryFilter": query_filter,
            "orderByNullPosition": order_by_null_position,
            "paginationSeed": pagination_seed,
        }

        params = format_api_params(param_dict)

        logger.info({"message": "Retrieving foods", "parameters": params})
        return self._handle_request("GET", "/api/foods", params=params)

    def create_food(self, food_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new food.

        Args:
            food_data: Dictionary containing food properties (name, pluralName, description, labelId, aliases)

        Returns:
            JSON response containing the created food
        """
        if not food_data or not food_data.get("name"):
            raise ValueError("Food name is required")

        logger.info({"message": "Creating food", "name": food_data.get("name")})
        return self._handle_request("POST", "/api/foods", json=food_data)

    def get_food(self, food_id: str) -> Dict[str, Any]:
        """Get a specific food by ID.

        Args:
            food_id: The UUID of the food

        Returns:
            JSON response containing the food details
        """
        if not food_id:
            raise ValueError("Food ID cannot be empty")

        logger.info({"message": "Retrieving food", "food_id": food_id})
        return self._handle_request("GET", f"/api/foods/{food_id}")

    def update_food(self, food_id: str, food_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific food.

        Args:
            food_id: The UUID of the food to update
            food_data: Dictionary containing the food properties to update

        Returns:
            JSON response containing the updated food
        """
        if not food_id:
            raise ValueError("Food ID cannot be empty")
        if not food_data:
            raise ValueError("Food data cannot be empty")

        logger.info({"message": "Updating food", "food_id": food_id})
        return self._handle_request("PUT", f"/api/foods/{food_id}", json=food_data)

    def delete_food(self, food_id: str) -> Dict[str, Any]:
        """Delete a specific food.

        Args:
            food_id: The UUID of the food to delete

        Returns:
            JSON response confirming deletion
        """
        if not food_id:
            raise ValueError("Food ID cannot be empty")

        logger.info({"message": "Deleting food", "food_id": food_id})
        return self._handle_request("DELETE", f"/api/foods/{food_id}")

    def merge_foods(self, from_food: str, to_food: str) -> Dict[str, Any]:
        """Merge one food into another. All references to from_food will be updated to to_food.

        Args:
            from_food: UUID of the food to merge from (will be deleted)
            to_food: UUID of the food to merge into (will be kept)

        Returns:
            JSON response confirming the merge
        """
        if not from_food or not to_food:
            raise ValueError("Both from_food and to_food IDs are required")

        payload = {"fromFood": from_food, "toFood": to_food}

        logger.info({"message": "Merging foods", "from": from_food, "to": to_food})
        return self._handle_request("PUT", "/api/foods/merge", json=payload)
