import logging
from typing import Any, Dict, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class LabelsMixin:
    """Mixin class for multi-purpose label API endpoints"""

    def get_labels(
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
        """Get all multi-purpose labels.

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            order_by: Field to order results by
            order_direction: Direction to order results ('asc' or 'desc')
            search: Search term to filter labels
            query_filter: Advanced query filter
            order_by_null_position: How to handle nulls in ordering ('first' or 'last')
            pagination_seed: Seed for consistent pagination

        Returns:
            JSON response containing label items and pagination information
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

        logger.info({"message": "Retrieving labels", "parameters": params})
        return self._handle_request("GET", "/api/groups/labels", params=params)

    def create_label(self, name: str, color: Optional[str] = None) -> Dict[str, Any]:
        """Create a new multi-purpose label.

        Args:
            name: Name of the label
            color: Hex color for the label (e.g., "#FF0000")

        Returns:
            JSON response containing the created label
        """
        if not name:
            raise ValueError("Label name cannot be empty")

        payload = {"name": name}
        if color:
            payload["color"] = color

        logger.info({"message": "Creating label", "name": name})
        return self._handle_request("POST", "/api/groups/labels", json=payload)

    def get_label(self, label_id: str) -> Dict[str, Any]:
        """Get a specific label by ID.

        Args:
            label_id: The UUID of the label

        Returns:
            JSON response containing the label details
        """
        if not label_id:
            raise ValueError("Label ID cannot be empty")

        logger.info({"message": "Retrieving label", "label_id": label_id})
        return self._handle_request("GET", f"/api/groups/labels/{label_id}")

    def update_label(self, label_id: str, label_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific label.

        Args:
            label_id: The UUID of the label to update
            label_data: Dictionary containing the label properties to update

        Returns:
            JSON response containing the updated label
        """
        if not label_id:
            raise ValueError("Label ID cannot be empty")
        if not label_data:
            raise ValueError("Label data cannot be empty")

        logger.info({"message": "Updating label", "label_id": label_id})
        return self._handle_request("PUT", f"/api/groups/labels/{label_id}", json=label_data)

    def delete_label(self, label_id: str) -> Dict[str, Any]:
        """Delete a specific label.

        Args:
            label_id: The UUID of the label to delete

        Returns:
            JSON response confirming deletion
        """
        if not label_id:
            raise ValueError("Label ID cannot be empty")

        logger.info({"message": "Deleting label", "label_id": label_id})
        return self._handle_request("DELETE", f"/api/groups/labels/{label_id}")
