import logging
import traceback
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_parser_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register all ingredient parser-related tools with the MCP server."""

    @mcp.tool()
    def parse_ingredient(
        ingredient: str,
        parser: str = "nlp",
    ) -> Dict[str, Any]:
        """Parse a single ingredient string into structured data (quantity, unit, food, note).
        Useful for converting free-text ingredients into structured recipe data.

        Args:
            ingredient: Ingredient string to parse (e.g., "2 cups all-purpose flour", "1/2 lb chicken breast, diced")
            parser: Parser engine to use - "nlp" (default, more accurate) or "brute" (faster, simpler)

        Returns:
            Dict[str, Any]: Parsed ingredient with quantity, unit, food, and other details
        """
        try:
            logger.info({"message": "Parsing ingredient", "ingredient": ingredient, "parser": parser})
            return mealie.parse_ingredient(ingredient, parser)
        except Exception as e:
            error_msg = f"Error parsing ingredient: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def parse_ingredients(
        ingredients: List[str],
        parser: str = "nlp",
    ) -> List[Dict[str, Any]]:
        """Parse multiple ingredient strings into structured data at once.

        Args:
            ingredients: List of ingredient strings to parse
            parser: Parser engine to use - "nlp" (default) or "brute"

        Returns:
            List[Dict[str, Any]]: List of parsed ingredients with quantity, unit, food, etc.
        """
        try:
            logger.info({"message": "Parsing ingredients", "count": len(ingredients), "parser": parser})
            return mealie.parse_ingredients(ingredients, parser)
        except Exception as e:
            error_msg = f"Error parsing ingredients: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
