import logging
from typing import Any, Dict, List

logger = logging.getLogger("mealie-mcp")


class ParserMixin:
    """Mixin class for ingredient parser API endpoints"""

    def parse_ingredient(self, ingredient: str, parser: str = "nlp") -> Dict[str, Any]:
        """Parse a single ingredient string into structured data.

        Args:
            ingredient: Ingredient string to parse (e.g., "2 cups all-purpose flour")
            parser: Parser to use ("nlp" or "brute")

        Returns:
            JSON response containing parsed ingredient data (quantity, unit, food, etc.)
        """
        if not ingredient:
            raise ValueError("Ingredient string cannot be empty")

        payload = {"parser": parser, "ingredient": ingredient}

        logger.info({"message": "Parsing ingredient", "ingredient": ingredient, "parser": parser})
        return self._handle_request("POST", "/api/parser/ingredient", json=payload)

    def parse_ingredients(self, ingredients: List[str], parser: str = "nlp") -> List[Dict[str, Any]]:
        """Parse multiple ingredient strings into structured data.

        Args:
            ingredients: List of ingredient strings to parse
            parser: Parser to use ("nlp" or "brute")

        Returns:
            List of parsed ingredient data
        """
        if not ingredients:
            raise ValueError("Ingredients list cannot be empty")

        payload = {"parser": parser, "ingredients": ingredients}

        logger.info({"message": "Parsing ingredients", "count": len(ingredients), "parser": parser})
        return self._handle_request("POST", "/api/parser/ingredients", json=payload)
