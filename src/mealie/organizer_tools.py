import logging
from typing import Any, Dict, List, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class OrganizerToolsMixin:
    """Mixin class for recipe tool/equipment-related API endpoints"""

    def get_organizer_tools(
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
        """Get all recipe tools/equipment.

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            order_by: Field to order results by
            order_direction: Direction to order results ('asc' or 'desc')
            search: Search term to filter tools
            query_filter: Advanced query filter
            order_by_null_position: How to handle nulls in ordering ('first' or 'last')
            pagination_seed: Seed for consistent pagination

        Returns:
            JSON response containing tool items and pagination information
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

        logger.info({"message": "Retrieving organizer tools", "parameters": params})
        return self._handle_request("GET", "/api/organizers/tools", params=params)

    def create_organizer_tool(self, name: str) -> Dict[str, Any]:
        """Create a new recipe tool/equipment.

        Args:
            name: Name of the tool

        Returns:
            JSON response containing the created tool
        """
        if not name:
            raise ValueError("Tool name cannot be empty")

        payload = {"name": name}

        logger.info({"message": "Creating organizer tool", "name": name})
        return self._handle_request("POST", "/api/organizers/tools", json=payload)

    def get_organizer_tool(self, tool_id: str) -> Dict[str, Any]:
        """Get a specific tool by ID.

        Args:
            tool_id: The UUID of the tool

        Returns:
            JSON response containing the tool details
        """
        if not tool_id:
            raise ValueError("Tool ID cannot be empty")

        logger.info({"message": "Retrieving organizer tool", "tool_id": tool_id})
        return self._handle_request("GET", f"/api/organizers/tools/{tool_id}")

    def get_organizer_tool_by_slug(self, tool_slug: str) -> Dict[str, Any]:
        """Get a specific tool by its slug.

        Args:
            tool_slug: The slug of the tool

        Returns:
            JSON response containing the tool details
        """
        if not tool_slug:
            raise ValueError("Tool slug cannot be empty")

        logger.info({"message": "Retrieving organizer tool by slug", "tool_slug": tool_slug})
        return self._handle_request("GET", f"/api/organizers/tools/slug/{tool_slug}")

    def update_organizer_tool(self, tool_id: str, tool_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific tool.

        Args:
            tool_id: The UUID of the tool to update
            tool_data: Dictionary containing the tool properties to update

        Returns:
            JSON response containing the updated tool
        """
        if not tool_id:
            raise ValueError("Tool ID cannot be empty")
        if not tool_data:
            raise ValueError("Tool data cannot be empty")

        logger.info({"message": "Updating organizer tool", "tool_id": tool_id})
        return self._handle_request("PUT", f"/api/organizers/tools/{tool_id}", json=tool_data)

    def delete_organizer_tool(self, tool_id: str) -> Dict[str, Any]:
        """Delete a specific tool.

        Args:
            tool_id: The UUID of the tool to delete

        Returns:
            JSON response confirming deletion
        """
        if not tool_id:
            raise ValueError("Tool ID cannot be empty")

        logger.info({"message": "Deleting organizer tool", "tool_id": tool_id})
        return self._handle_request("DELETE", f"/api/organizers/tools/{tool_id}")
