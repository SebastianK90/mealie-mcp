import logging
from typing import Any, Dict, List, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class UnitsMixin:
    """Mixin class for unit-related API endpoints"""

    def get_units(
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
        """Get all units.

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            order_by: Field to order results by
            order_direction: Direction to order results ('asc' or 'desc')
            search: Search term to filter units
            query_filter: Advanced query filter
            order_by_null_position: How to handle nulls in ordering ('first' or 'last')
            pagination_seed: Seed for consistent pagination

        Returns:
            JSON response containing unit items and pagination information
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

        logger.info({"message": "Retrieving units", "parameters": params})
        return self._handle_request("GET", "/api/units", params=params)

    def create_unit(self, unit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new unit.

        Args:
            unit_data: Dictionary containing unit properties (name, pluralName, abbreviation, fraction, useAbbreviation, aliases)

        Returns:
            JSON response containing the created unit
        """
        if not unit_data or not unit_data.get("name"):
            raise ValueError("Unit name is required")

        logger.info({"message": "Creating unit", "name": unit_data.get("name")})
        return self._handle_request("POST", "/api/units", json=unit_data)

    def get_unit(self, unit_id: str) -> Dict[str, Any]:
        """Get a specific unit by ID.

        Args:
            unit_id: The UUID of the unit

        Returns:
            JSON response containing the unit details
        """
        if not unit_id:
            raise ValueError("Unit ID cannot be empty")

        logger.info({"message": "Retrieving unit", "unit_id": unit_id})
        return self._handle_request("GET", f"/api/units/{unit_id}")

    def update_unit(self, unit_id: str, unit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific unit.

        Args:
            unit_id: The UUID of the unit to update
            unit_data: Dictionary containing the unit properties to update

        Returns:
            JSON response containing the updated unit
        """
        if not unit_id:
            raise ValueError("Unit ID cannot be empty")
        if not unit_data:
            raise ValueError("Unit data cannot be empty")

        logger.info({"message": "Updating unit", "unit_id": unit_id})
        return self._handle_request("PUT", f"/api/units/{unit_id}", json=unit_data)

    def delete_unit(self, unit_id: str) -> Dict[str, Any]:
        """Delete a specific unit.

        Args:
            unit_id: The UUID of the unit to delete

        Returns:
            JSON response confirming deletion
        """
        if not unit_id:
            raise ValueError("Unit ID cannot be empty")

        logger.info({"message": "Deleting unit", "unit_id": unit_id})
        return self._handle_request("DELETE", f"/api/units/{unit_id}")

    def merge_units(self, from_unit: str, to_unit: str) -> Dict[str, Any]:
        """Merge one unit into another. All references to from_unit will be updated to to_unit.

        Args:
            from_unit: UUID of the unit to merge from (will be deleted)
            to_unit: UUID of the unit to merge into (will be kept)

        Returns:
            JSON response confirming the merge
        """
        if not from_unit or not to_unit:
            raise ValueError("Both from_unit and to_unit IDs are required")

        payload = {"fromUnit": from_unit, "toUnit": to_unit}

        logger.info({"message": "Merging units", "from": from_unit, "to": to_unit})
        return self._handle_request("PUT", "/api/units/merge", json=payload)
