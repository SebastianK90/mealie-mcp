import logging
import traceback
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_units_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register all unit-related tools with the MCP server."""

    @mcp.tool()
    def get_units(
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get all measurement units with pagination and search. Units are used for recipe ingredients
        and shopping list items (e.g., "cup", "tablespoon", "pound").

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            search: Search term to filter units by name

        Returns:
            Dict[str, Any]: Units with pagination information
        """
        try:
            logger.info({"message": "Fetching units", "page": page, "per_page": per_page, "search": search})
            return mealie.get_units(page=page, per_page=per_page, search=search)
        except Exception as e:
            error_msg = f"Error fetching units: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def create_unit(
        name: str,
        plural_name: Optional[str] = None,
        abbreviation: Optional[str] = None,
        use_abbreviation: Optional[bool] = None,
        fraction: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Create a new measurement unit.

        Args:
            name: Name of the unit (e.g., "cup", "tablespoon", "pound")
            plural_name: Plural form (e.g., "cups", "tablespoons", "pounds")
            abbreviation: Short form (e.g., "c", "tbsp", "lb")
            use_abbreviation: Whether to display the abbreviation instead of the full name
            fraction: Whether to display quantities as fractions (e.g., 1/2 instead of 0.5)

        Returns:
            Dict[str, Any]: The created unit details including its ID
        """
        try:
            logger.info({"message": "Creating unit", "name": name})
            unit_data = {"name": name}
            if plural_name is not None:
                unit_data["pluralName"] = plural_name
            if abbreviation is not None:
                unit_data["abbreviation"] = abbreviation
            if use_abbreviation is not None:
                unit_data["useAbbreviation"] = use_abbreviation
            if fraction is not None:
                unit_data["fraction"] = fraction
            return mealie.create_unit(unit_data)
        except Exception as e:
            error_msg = f"Error creating unit '{name}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_unit(unit_id: str) -> Dict[str, Any]:
        """Get a specific measurement unit by ID.

        Args:
            unit_id: The UUID of the unit

        Returns:
            Dict[str, Any]: The unit details
        """
        try:
            logger.info({"message": "Fetching unit", "unit_id": unit_id})
            return mealie.get_unit(unit_id)
        except Exception as e:
            error_msg = f"Error fetching unit '{unit_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_unit(
        unit_id: str,
        name: Optional[str] = None,
        plural_name: Optional[str] = None,
        abbreviation: Optional[str] = None,
        use_abbreviation: Optional[bool] = None,
        fraction: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Update a measurement unit's details.

        Args:
            unit_id: The UUID of the unit to update
            name: New name for the unit
            plural_name: New plural name
            abbreviation: New abbreviation
            use_abbreviation: Whether to use abbreviation
            fraction: Whether to display as fractions

        Returns:
            Dict[str, Any]: The updated unit details
        """
        try:
            logger.info({"message": "Updating unit", "unit_id": unit_id})

            unit_data = {}
            if name is not None:
                unit_data["name"] = name
            if plural_name is not None:
                unit_data["pluralName"] = plural_name
            if abbreviation is not None:
                unit_data["abbreviation"] = abbreviation
            if use_abbreviation is not None:
                unit_data["useAbbreviation"] = use_abbreviation
            if fraction is not None:
                unit_data["fraction"] = fraction

            if not unit_data:
                raise ValueError("At least one field must be provided to update")

            return mealie.update_unit(unit_id, unit_data)
        except Exception as e:
            error_msg = f"Error updating unit '{unit_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def delete_unit(unit_id: str) -> Dict[str, Any]:
        """Delete a specific measurement unit.

        Args:
            unit_id: The UUID of the unit to delete

        Returns:
            Dict[str, Any]: Confirmation of deletion
        """
        try:
            logger.info({"message": "Deleting unit", "unit_id": unit_id})
            return mealie.delete_unit(unit_id)
        except Exception as e:
            error_msg = f"Error deleting unit '{unit_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def merge_units(from_unit: str, to_unit: str) -> Dict[str, Any]:
        """Merge one unit into another. All recipe ingredients and shopping list items referencing
        from_unit will be updated to reference to_unit. The from_unit will be deleted.

        Args:
            from_unit: UUID of the unit to merge from (will be deleted)
            to_unit: UUID of the unit to merge into (will be kept)

        Returns:
            Dict[str, Any]: Confirmation of the merge
        """
        try:
            logger.info({"message": "Merging units", "from": from_unit, "to": to_unit})
            return mealie.merge_units(from_unit, to_unit)
        except Exception as e:
            error_msg = f"Error merging units: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
