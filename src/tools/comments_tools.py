import logging
import traceback
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_comments_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register all recipe comment-related tools with the MCP server."""

    @mcp.tool()
    def get_recipe_comments(recipe_slug: str) -> List[Dict[str, Any]]:
        """Get all comments for a specific recipe.

        Args:
            recipe_slug: The slug identifier of the recipe

        Returns:
            List[Dict[str, Any]]: List of comments on the recipe
        """
        try:
            logger.info({"message": "Fetching recipe comments", "slug": recipe_slug})
            return mealie.get_recipe_comments(recipe_slug)
        except Exception as e:
            error_msg = f"Error fetching comments for recipe '{recipe_slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def create_comment(recipe_id: str, text: str) -> Dict[str, Any]:
        """Add a comment to a recipe.

        Args:
            recipe_id: The UUID of the recipe to comment on (use get_recipe_detailed to find the ID)
            text: The comment text

        Returns:
            Dict[str, Any]: The created comment details
        """
        try:
            logger.info({"message": "Creating comment", "recipe_id": recipe_id})
            return mealie.create_comment(recipe_id, text)
        except Exception as e:
            error_msg = f"Error creating comment: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_comment(comment_id: str, text: str) -> Dict[str, Any]:
        """Update an existing comment's text.

        Args:
            comment_id: The UUID of the comment to update
            text: The updated comment text

        Returns:
            Dict[str, Any]: The updated comment details
        """
        try:
            logger.info({"message": "Updating comment", "comment_id": comment_id})
            return mealie.update_comment(comment_id, text)
        except Exception as e:
            error_msg = f"Error updating comment '{comment_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def delete_comment(comment_id: str) -> Dict[str, Any]:
        """Delete a comment from a recipe.

        Args:
            comment_id: The UUID of the comment to delete

        Returns:
            Dict[str, Any]: Confirmation of deletion
        """
        try:
            logger.info({"message": "Deleting comment", "comment_id": comment_id})
            return mealie.delete_comment(comment_id)
        except Exception as e:
            error_msg = f"Error deleting comment '{comment_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
