import logging
from typing import Any, Dict

logger = logging.getLogger("mealie-mcp")


class GroupMixin:
    """Mixin class for group and household-related API endpoints"""

    def get_current_group(self) -> Dict[str, Any]:
        """Get information about the current user's group.

        Returns:
            Dictionary containing group details such as id, name, slug, and other group information.
        """
        logger.info({"message": "Retrieving current group information"})
        return self._handle_request("GET", "/api/groups/self")

    def get_household_statistics(self) -> Dict[str, Any]:
        """Get statistics for the current household.

        Returns:
            Dictionary containing stats like totalRecipes, totalUsers, totalCategories, etc.
        """
        logger.info({"message": "Retrieving household statistics"})
        return self._handle_request("GET", "/api/households/statistics")
