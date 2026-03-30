import logging
import traceback
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_organizer_tools_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register all recipe tool/equipment-related tools with the MCP server."""

    @mcp.tool()
    def get_tools(
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get all recipe tools/equipment with pagination and search. Tools represent kitchen
        equipment needed for recipes (e.g., "Oven", "Blender", "Stand Mixer").

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            search: Search term to filter tools by name

        Returns:
            Dict[str, Any]: Tools with pagination information
        """
        try:
            logger.info({"message": "Fetching tools", "page": page, "per_page": per_page, "search": search})
            return mealie.get_organizer_tools(page=page, per_page=per_page, search=search)
        except Exception as e:
            error_msg = f"Error fetching tools: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def create_tool(name: str) -> Dict[str, Any]:
        """Create a new recipe tool/equipment entry.

        Args:
            name: Name of the tool (e.g., "Oven", "Blender", "Cast Iron Skillet")

        Returns:
            Dict[str, Any]: The created tool details including its ID and slug
        """
        try:
            logger.info({"message": "Creating tool", "name": name})
            return mealie.create_organizer_tool(name)
        except Exception as e:
            error_msg = f"Error creating tool '{name}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_tool(tool_id: str) -> Dict[str, Any]:
        """Get a specific recipe tool by ID.

        Args:
            tool_id: The UUID of the tool

        Returns:
            Dict[str, Any]: The tool details including associated recipes
        """
        try:
            logger.info({"message": "Fetching tool", "tool_id": tool_id})
            return mealie.get_organizer_tool(tool_id)
        except Exception as e:
            error_msg = f"Error fetching tool '{tool_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_tool_by_slug(tool_slug: str) -> Dict[str, Any]:
        """Get a specific recipe tool by its slug.

        Args:
            tool_slug: The slug of the tool (e.g., "oven", "blender")

        Returns:
            Dict[str, Any]: The tool details including associated recipes
        """
        try:
            logger.info({"message": "Fetching tool by slug", "tool_slug": tool_slug})
            return mealie.get_organizer_tool_by_slug(tool_slug)
        except Exception as e:
            error_msg = f"Error fetching tool by slug '{tool_slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_tool(
        tool_id: str,
        name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a recipe tool's name.

        Args:
            tool_id: The UUID of the tool to update
            name: New name for the tool

        Returns:
            Dict[str, Any]: The updated tool details
        """
        try:
            logger.info({"message": "Updating tool", "tool_id": tool_id})

            tool_data = {}
            if name is not None:
                tool_data["name"] = name

            if not tool_data:
                raise ValueError("At least one field must be provided to update")

            return mealie.update_organizer_tool(tool_id, tool_data)
        except Exception as e:
            error_msg = f"Error updating tool '{tool_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def delete_tool(tool_id: str) -> Dict[str, Any]:
        """Delete a specific recipe tool.

        Args:
            tool_id: The UUID of the tool to delete

        Returns:
            Dict[str, Any]: Confirmation of deletion
        """
        try:
            logger.info({"message": "Deleting tool", "tool_id": tool_id})
            return mealie.delete_organizer_tool(tool_id)
        except Exception as e:
            error_msg = f"Error deleting tool '{tool_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
