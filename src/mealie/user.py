import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("mealie-mcp")


class UserMixin:
    """Mixin class for user-related API endpoints"""

    def get_current_user(self) -> Dict[str, Any]:
        """Get information about the currently logged in user.

        Returns:
            Dictionary containing user details such as id, username, email, and other profile information.
        """
        logger.info({"message": "Retrieving current user information"})
        return self._handle_request("GET", "/api/users/self")

    def get_user_favorites(self) -> List[Dict[str, Any]]:
        """Get the current user's favorite recipes.

        Returns:
            List of favorite recipe summaries
        """
        logger.info({"message": "Retrieving user favorites"})
        return self._handle_request("GET", "/api/users/self/favorites")

    def get_user_ratings(self) -> List[Dict[str, Any]]:
        """Get the current user's recipe ratings.

        Returns:
            List of recipe ratings
        """
        logger.info({"message": "Retrieving user ratings"})
        return self._handle_request("GET", "/api/users/self/ratings")

    def add_favorite(self, user_id: str, recipe_slug: str) -> Dict[str, Any]:
        """Add a recipe to the user's favorites.

        Args:
            user_id: The UUID of the user
            recipe_slug: The slug of the recipe to favorite

        Returns:
            JSON response confirming the favorite was added
        """
        if not user_id or not recipe_slug:
            raise ValueError("User ID and recipe slug are required")

        logger.info({"message": "Adding favorite", "user_id": user_id, "slug": recipe_slug})
        return self._handle_request("POST", f"/api/users/{user_id}/favorites/{recipe_slug}")

    def remove_favorite(self, user_id: str, recipe_slug: str) -> Dict[str, Any]:
        """Remove a recipe from the user's favorites.

        Args:
            user_id: The UUID of the user
            recipe_slug: The slug of the recipe to unfavorite

        Returns:
            JSON response confirming the favorite was removed
        """
        if not user_id or not recipe_slug:
            raise ValueError("User ID and recipe slug are required")

        logger.info({"message": "Removing favorite", "user_id": user_id, "slug": recipe_slug})
        return self._handle_request("DELETE", f"/api/users/{user_id}/favorites/{recipe_slug}")

    def set_rating(
        self, user_id: str, recipe_slug: str,
        rating: Optional[float] = None, is_favorite: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Set a rating and/or favorite status for a recipe.

        Args:
            user_id: The UUID of the user
            recipe_slug: The slug of the recipe to rate
            rating: Rating value (0-5, or None to clear)
            is_favorite: Whether to mark as favorite

        Returns:
            JSON response confirming the rating was set
        """
        if not user_id or not recipe_slug:
            raise ValueError("User ID and recipe slug are required")

        payload = {}
        if rating is not None:
            payload["rating"] = rating
        if is_favorite is not None:
            payload["isFavorite"] = is_favorite

        logger.info({"message": "Setting rating", "user_id": user_id, "slug": recipe_slug})
        return self._handle_request("POST", f"/api/users/{user_id}/ratings/{recipe_slug}", json=payload)
