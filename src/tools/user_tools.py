import logging
import traceback
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_user_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register all user-related tools with the MCP server."""

    @mcp.tool()
    def get_current_user() -> Dict[str, Any]:
        """Get information about the currently logged-in user, including their ID, username,
        email, group, and household.

        Returns:
            Dict[str, Any]: Current user details
        """
        try:
            logger.info({"message": "Fetching current user"})
            return mealie.get_current_user()
        except Exception as e:
            error_msg = f"Error fetching current user: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_user_favorites() -> List[Dict[str, Any]]:
        """Get the current user's favorite recipes.

        Returns:
            List[Dict[str, Any]]: List of favorited recipe summaries
        """
        try:
            logger.info({"message": "Fetching user favorites"})
            return mealie.get_user_favorites()
        except Exception as e:
            error_msg = f"Error fetching user favorites: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_user_ratings() -> List[Dict[str, Any]]:
        """Get the current user's recipe ratings.

        Returns:
            List[Dict[str, Any]]: List of recipe ratings
        """
        try:
            logger.info({"message": "Fetching user ratings"})
            return mealie.get_user_ratings()
        except Exception as e:
            error_msg = f"Error fetching user ratings: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def add_favorite(recipe_slug: str) -> Dict[str, Any]:
        """Add a recipe to the current user's favorites.

        Args:
            recipe_slug: The slug of the recipe to favorite

        Returns:
            Dict[str, Any]: Confirmation that the recipe was favorited
        """
        try:
            logger.info({"message": "Adding favorite", "slug": recipe_slug})
            user = mealie.get_current_user()
            return mealie.add_favorite(user["id"], recipe_slug)
        except Exception as e:
            error_msg = f"Error adding favorite '{recipe_slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def remove_favorite(recipe_slug: str) -> Dict[str, Any]:
        """Remove a recipe from the current user's favorites.

        Args:
            recipe_slug: The slug of the recipe to unfavorite

        Returns:
            Dict[str, Any]: Confirmation that the recipe was unfavorited
        """
        try:
            logger.info({"message": "Removing favorite", "slug": recipe_slug})
            user = mealie.get_current_user()
            return mealie.remove_favorite(user["id"], recipe_slug)
        except Exception as e:
            error_msg = f"Error removing favorite '{recipe_slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def set_recipe_rating(
        recipe_slug: str,
        rating: Optional[float] = None,
        is_favorite: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Set a rating and/or favorite status for a recipe.

        Args:
            recipe_slug: The slug of the recipe to rate
            rating: Rating value from 0 to 5 (use None to clear the rating)
            is_favorite: Whether to mark the recipe as a favorite

        Returns:
            Dict[str, Any]: Confirmation of the rating
        """
        try:
            logger.info({"message": "Setting recipe rating", "slug": recipe_slug, "rating": rating})
            user = mealie.get_current_user()
            return mealie.set_rating(user["id"], recipe_slug, rating, is_favorite)
        except Exception as e:
            error_msg = f"Error setting rating for '{recipe_slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_household_statistics() -> Dict[str, Any]:
        """Get statistics for the current household including total recipes, users, categories, tags, and tools.

        Returns:
            Dict[str, Any]: Household statistics
        """
        try:
            logger.info({"message": "Fetching household statistics"})
            return mealie.get_household_statistics()
        except Exception as e:
            error_msg = f"Error fetching household statistics: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
