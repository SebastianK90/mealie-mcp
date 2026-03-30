import logging
import traceback
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_foods_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register all food-related tools with the MCP server."""

    @mcp.tool()
    def get_foods(
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get all foods with pagination and search. Foods represent ingredients in the database
        and are used to link shopping list items to recipe ingredients.

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            search: Search term to filter foods by name

        Returns:
            Dict[str, Any]: Foods with pagination information
        """
        try:
            logger.info({"message": "Fetching foods", "page": page, "per_page": per_page, "search": search})
            return mealie.get_foods(page=page, per_page=per_page, search=search)
        except Exception as e:
            error_msg = f"Error fetching foods: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def create_food(
        name: str,
        plural_name: Optional[str] = None,
        description: Optional[str] = None,
        label_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new food item in the database.

        Args:
            name: Name of the food (e.g., "Chicken Breast", "Olive Oil")
            plural_name: Plural form of the name (e.g., "Chicken Breasts")
            description: Description of the food
            label_id: UUID of the label to categorize this food (e.g., Produce, Dairy)

        Returns:
            Dict[str, Any]: The created food details including its ID
        """
        try:
            logger.info({"message": "Creating food", "name": name})
            food_data = {"name": name}
            if plural_name is not None:
                food_data["pluralName"] = plural_name
            if description is not None:
                food_data["description"] = description
            if label_id is not None:
                food_data["labelId"] = label_id
            return mealie.create_food(food_data)
        except Exception as e:
            error_msg = f"Error creating food '{name}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_food(food_id: str) -> Dict[str, Any]:
        """Get a specific food by ID.

        Args:
            food_id: The UUID of the food

        Returns:
            Dict[str, Any]: The food details
        """
        try:
            logger.info({"message": "Fetching food", "food_id": food_id})
            return mealie.get_food(food_id)
        except Exception as e:
            error_msg = f"Error fetching food '{food_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_food(
        food_id: str,
        name: Optional[str] = None,
        plural_name: Optional[str] = None,
        description: Optional[str] = None,
        label_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a food item's details.

        Args:
            food_id: The UUID of the food to update
            name: New name for the food
            plural_name: New plural name
            description: New description
            label_id: New label UUID

        Returns:
            Dict[str, Any]: The updated food details
        """
        try:
            logger.info({"message": "Updating food", "food_id": food_id})

            food_data = {}
            if name is not None:
                food_data["name"] = name
            if plural_name is not None:
                food_data["pluralName"] = plural_name
            if description is not None:
                food_data["description"] = description
            if label_id is not None:
                food_data["labelId"] = label_id

            if not food_data:
                raise ValueError("At least one field must be provided to update")

            return mealie.update_food(food_id, food_data)
        except Exception as e:
            error_msg = f"Error updating food '{food_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def delete_food(food_id: str) -> Dict[str, Any]:
        """Delete a specific food.

        Args:
            food_id: The UUID of the food to delete

        Returns:
            Dict[str, Any]: Confirmation of deletion
        """
        try:
            logger.info({"message": "Deleting food", "food_id": food_id})
            return mealie.delete_food(food_id)
        except Exception as e:
            error_msg = f"Error deleting food '{food_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def merge_foods(from_food: str, to_food: str) -> Dict[str, Any]:
        """Merge one food into another. All recipe ingredients and shopping list items referencing
        from_food will be updated to reference to_food. The from_food will be deleted.

        Args:
            from_food: UUID of the food to merge from (will be deleted)
            to_food: UUID of the food to merge into (will be kept)

        Returns:
            Dict[str, Any]: Confirmation of the merge
        """
        try:
            logger.info({"message": "Merging foods", "from": from_food, "to": to_food})
            return mealie.merge_foods(from_food, to_food)
        except Exception as e:
            error_msg = f"Error merging foods: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
