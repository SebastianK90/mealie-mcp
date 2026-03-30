import logging
from typing import Any, Dict, List, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class CookbooksMixin:
    """Mixin class for cookbook-related API endpoints"""

    def get_cookbooks(
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
        """Get all cookbooks for the current household.

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            order_by: Field to order results by
            order_direction: Direction to order results ('asc' or 'desc')
            search: Search term to filter cookbooks
            query_filter: Advanced query filter
            order_by_null_position: How to handle nulls in ordering ('first' or 'last')
            pagination_seed: Seed for consistent pagination

        Returns:
            JSON response containing cookbook items and pagination information
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

        logger.info({"message": "Retrieving cookbooks", "parameters": params})
        return self._handle_request("GET", "/api/households/cookbooks", params=params)

    def create_cookbook(self, cookbook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new cookbook.

        Args:
            cookbook_data: Dictionary containing cookbook properties (name, description, slug, public, queryFilterString)

        Returns:
            JSON response containing the created cookbook
        """
        if not cookbook_data or not cookbook_data.get("name"):
            raise ValueError("Cookbook name is required")

        logger.info({"message": "Creating cookbook", "name": cookbook_data.get("name")})
        return self._handle_request("POST", "/api/households/cookbooks", json=cookbook_data)

    def get_cookbook(self, cookbook_id: str) -> Dict[str, Any]:
        """Get a specific cookbook by ID.

        Args:
            cookbook_id: The UUID of the cookbook

        Returns:
            JSON response containing the cookbook details
        """
        if not cookbook_id:
            raise ValueError("Cookbook ID cannot be empty")

        logger.info({"message": "Retrieving cookbook", "cookbook_id": cookbook_id})
        return self._handle_request("GET", f"/api/households/cookbooks/{cookbook_id}")

    def update_cookbook(self, cookbook_id: str, cookbook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific cookbook.

        Args:
            cookbook_id: The UUID of the cookbook to update
            cookbook_data: Dictionary containing the cookbook properties to update

        Returns:
            JSON response containing the updated cookbook
        """
        if not cookbook_id:
            raise ValueError("Cookbook ID cannot be empty")
        if not cookbook_data:
            raise ValueError("Cookbook data cannot be empty")

        logger.info({"message": "Updating cookbook", "cookbook_id": cookbook_id})
        return self._handle_request("PUT", f"/api/households/cookbooks/{cookbook_id}", json=cookbook_data)

    def delete_cookbook(self, cookbook_id: str) -> Dict[str, Any]:
        """Delete a specific cookbook.

        Args:
            cookbook_id: The UUID of the cookbook to delete

        Returns:
            JSON response confirming deletion
        """
        if not cookbook_id:
            raise ValueError("Cookbook ID cannot be empty")

        logger.info({"message": "Deleting cookbook", "cookbook_id": cookbook_id})
        return self._handle_request("DELETE", f"/api/households/cookbooks/{cookbook_id}")
