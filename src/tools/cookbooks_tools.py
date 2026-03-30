import logging
import traceback
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_cookbooks_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register all cookbook-related tools with the MCP server."""

    @mcp.tool()
    def get_cookbooks(
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get all cookbooks for the current household. Cookbooks are curated collections
        of recipes filtered by a query string.

        Args:
            page: Page number to retrieve
            per_page: Number of items per page

        Returns:
            Dict[str, Any]: Cookbooks with pagination information
        """
        try:
            logger.info({"message": "Fetching cookbooks", "page": page, "per_page": per_page})
            return mealie.get_cookbooks(page=page, per_page=per_page)
        except Exception as e:
            error_msg = f"Error fetching cookbooks: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def create_cookbook(
        name: str,
        description: Optional[str] = None,
        public: Optional[bool] = None,
        query_filter_string: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new cookbook. Cookbooks are collections of recipes filtered by a query.

        Args:
            name: Name of the cookbook (e.g., "Weeknight Dinners", "Holiday Baking")
            description: Description of the cookbook
            public: Whether the cookbook is publicly accessible
            query_filter_string: Filter query to select recipes for this cookbook (same syntax as recipe queryFilter)

        Returns:
            Dict[str, Any]: The created cookbook details including its ID
        """
        try:
            logger.info({"message": "Creating cookbook", "name": name})
            cookbook_data = {"name": name}
            if description is not None:
                cookbook_data["description"] = description
            if public is not None:
                cookbook_data["public"] = public
            if query_filter_string is not None:
                cookbook_data["queryFilterString"] = query_filter_string
            return mealie.create_cookbook(cookbook_data)
        except Exception as e:
            error_msg = f"Error creating cookbook '{name}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_cookbook(cookbook_id: str) -> Dict[str, Any]:
        """Get a specific cookbook by ID, including its recipe collection.

        Args:
            cookbook_id: The UUID of the cookbook

        Returns:
            Dict[str, Any]: The cookbook details including recipes
        """
        try:
            logger.info({"message": "Fetching cookbook", "cookbook_id": cookbook_id})
            return mealie.get_cookbook(cookbook_id)
        except Exception as e:
            error_msg = f"Error fetching cookbook '{cookbook_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_cookbook(
        cookbook_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        public: Optional[bool] = None,
        query_filter_string: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a cookbook's details.

        Args:
            cookbook_id: The UUID of the cookbook to update
            name: New name for the cookbook
            description: New description
            public: Whether the cookbook should be public
            query_filter_string: New filter query for selecting recipes

        Returns:
            Dict[str, Any]: The updated cookbook details
        """
        try:
            logger.info({"message": "Updating cookbook", "cookbook_id": cookbook_id})

            cookbook_data = {}
            if name is not None:
                cookbook_data["name"] = name
            if description is not None:
                cookbook_data["description"] = description
            if public is not None:
                cookbook_data["public"] = public
            if query_filter_string is not None:
                cookbook_data["queryFilterString"] = query_filter_string

            if not cookbook_data:
                raise ValueError("At least one field must be provided to update")

            return mealie.update_cookbook(cookbook_id, cookbook_data)
        except Exception as e:
            error_msg = f"Error updating cookbook '{cookbook_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def delete_cookbook(cookbook_id: str) -> Dict[str, Any]:
        """Delete a specific cookbook. This does not delete the recipes in the cookbook.

        Args:
            cookbook_id: The UUID of the cookbook to delete

        Returns:
            Dict[str, Any]: Confirmation of deletion
        """
        try:
            logger.info({"message": "Deleting cookbook", "cookbook_id": cookbook_id})
            return mealie.delete_cookbook(cookbook_id)
        except Exception as e:
            error_msg = f"Error deleting cookbook '{cookbook_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
