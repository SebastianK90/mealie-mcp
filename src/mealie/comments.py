import logging
from typing import Any, Dict, List, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class CommentsMixin:
    """Mixin class for recipe comment-related API endpoints"""

    def get_recipe_comments(self, recipe_slug: str) -> List[Dict[str, Any]]:
        """Get all comments for a specific recipe.

        Args:
            recipe_slug: The slug identifier of the recipe

        Returns:
            List of comment objects
        """
        if not recipe_slug:
            raise ValueError("Recipe slug cannot be empty")

        logger.info({"message": "Retrieving recipe comments", "slug": recipe_slug})
        return self._handle_request("GET", f"/api/recipes/{recipe_slug}/comments")

    def create_comment(self, recipe_id: str, text: str) -> Dict[str, Any]:
        """Create a new comment on a recipe.

        Args:
            recipe_id: The UUID of the recipe to comment on
            text: The comment text

        Returns:
            JSON response containing the created comment
        """
        if not recipe_id:
            raise ValueError("Recipe ID cannot be empty")
        if not text:
            raise ValueError("Comment text cannot be empty")

        payload = {"recipeId": recipe_id, "text": text}

        logger.info({"message": "Creating comment", "recipe_id": recipe_id})
        return self._handle_request("POST", "/api/comments", json=payload)

    def update_comment(self, comment_id: str, text: str) -> Dict[str, Any]:
        """Update an existing comment.

        Args:
            comment_id: The UUID of the comment to update
            text: The updated comment text

        Returns:
            JSON response containing the updated comment
        """
        if not comment_id:
            raise ValueError("Comment ID cannot be empty")
        if not text:
            raise ValueError("Comment text cannot be empty")

        payload = {"text": text}

        logger.info({"message": "Updating comment", "comment_id": comment_id})
        return self._handle_request("PUT", f"/api/comments/{comment_id}", json=payload)

    def delete_comment(self, comment_id: str) -> Dict[str, Any]:
        """Delete a comment.

        Args:
            comment_id: The UUID of the comment to delete

        Returns:
            JSON response confirming deletion
        """
        if not comment_id:
            raise ValueError("Comment ID cannot be empty")

        logger.info({"message": "Deleting comment", "comment_id": comment_id})
        return self._handle_request("DELETE", f"/api/comments/{comment_id}")
