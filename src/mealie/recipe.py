import logging
from typing import Any, Dict, List, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class RecipeMixin:
    """Mixin class for recipe-related API endpoints"""

    def get_recipes(
        self,
        search: Optional[str] = None,
        order_by: Optional[str] = None,
        order_by_null_position: Optional[str] = None,
        order_direction: Optional[str] = "desc",
        query_filter: Optional[str] = None,
        pagination_seed: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        tools: Optional[List[str]] = None,
        require_all_tags: Optional[bool] = None,
        require_all_categories: Optional[bool] = None,
        require_all_tools: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Provides paginated list of recipes

        Args:
            search: Search term to filter recipes by name, description, etc.
            order_by: Field to order results by
            order_by_null_position: How to handle nulls in ordering ('first' or 'last')
            order_direction: Direction to order results ('asc' or 'desc')
            query_filter: Advanced query filter
            pagination_seed: Seed for consistent pagination
            page: Page number to retrieve
            per_page: Number of items per page
            categories: List of category slugs (NOT names) to filter by
            tags: List of tag slugs or UUIDs (NOT display names) to filter by
            tools: List of tool slugs to filter by
            require_all_tags: If True, recipe must have ALL specified tags (AND logic). Default False (OR logic)
            require_all_categories: If True, recipe must have ALL specified categories (AND logic)
            require_all_tools: If True, recipe must have ALL specified tools (AND logic)

        Returns:
            JSON response containing recipe items and pagination information
        """

        param_dict = {
            "search": search,
            "orderBy": order_by,
            "orderByNullPosition": order_by_null_position,
            "orderDirection": order_direction,
            "queryFilter": query_filter,
            "paginationSeed": pagination_seed,
            "page": page,
            "perPage": per_page,
            "categories": categories,
            "tags": tags,
            "tools": tools,
            "requireAllTags": require_all_tags,
            "requireAllCategories": require_all_categories,
            "requireAllTools": require_all_tools,
        }

        params = format_api_params(param_dict)

        logger.info({"message": "Retrieving recipes", "parameters": params})
        return self._handle_request("GET", "/api/recipes", params=params)

    def get_recipe(self, slug: str) -> Dict[str, Any]:
        """Retrieve a specific recipe by its slug

        Args:
            slug: The slug identifier of the recipe to retrieve

        Returns:
            JSON response containing all recipe details
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")

        logger.info({"message": "Retrieving recipe", "slug": slug})
        return self._handle_request("GET", f"/api/recipes/{slug}")

    def update_recipe(self, slug: str, recipe_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific recipe by its slug

        Args:
            slug: The slug identifier of the recipe to update
            recipe_data: Dictionary containing the recipe properties to update

        Returns:
            JSON response containing the updated recipe details
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")
        if not recipe_data:
            raise ValueError("Recipe data cannot be empty")

        logger.info({"message": "Updating recipe", "slug": slug})
        return self._handle_request("PUT", f"/api/recipes/{slug}", json=recipe_data)

    def create_recipe(self, name: str) -> str:
        """Create a new recipe

        Args:
            name: The name of the new recipe

        Returns:
            Slug of the newly created recipe
        """
        logger.info({"message": "Creating new recipe", "name": name})
        return self._handle_request("POST", "/api/recipes", json={"name": name})

    def patch_recipe(self, slug: str, recipe_data: Dict[str, Any]) -> Dict[str, Any]:
        """Partially update a recipe (only updates provided fields)

        Args:
            slug: The slug identifier of the recipe to patch
            recipe_data: Dictionary containing only the fields to update

        Returns:
            JSON response containing the updated recipe details
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")
        if not recipe_data:
            raise ValueError("Recipe data cannot be empty")

        logger.info({"message": "Patching recipe", "slug": slug})
        return self._handle_request("PATCH", f"/api/recipes/{slug}", json=recipe_data)

    def duplicate_recipe(self, slug: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Duplicate an existing recipe

        Args:
            slug: The slug identifier of the recipe to duplicate
            name: Optional new name for the duplicate (defaults to original name + copy indicator)

        Returns:
            JSON response containing the newly created duplicate recipe
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")

        payload = {}
        if name:
            payload["name"] = name

        logger.info({"message": "Duplicating recipe", "slug": slug})
        return self._handle_request("POST", f"/api/recipes/{slug}/duplicate", json=payload)

    def update_recipe_last_made(self, slug: str, timestamp: Optional[str] = None) -> Dict[str, Any]:
        """Update the last made timestamp for a recipe

        Args:
            slug: The slug identifier of the recipe
            timestamp: ISO format timestamp (if None, uses current time)

        Returns:
            JSON response containing the updated recipe
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")

        # If no timestamp provided, use current time
        if not timestamp:
            from datetime import datetime
            timestamp = datetime.utcnow().isoformat() + "Z"

        payload = {"timestamp": timestamp}

        logger.info({"message": "Updating recipe last made", "slug": slug})
        return self._handle_request("PATCH", f"/api/recipes/{slug}/last-made", json=payload)

    def scrape_recipe_image_from_url(self, slug: str, image_url: str) -> Dict[str, Any]:
        """Scrape and set a recipe's image from a URL (JSON payload)

        Args:
            slug: The slug identifier of the recipe
            image_url: URL of the image to scrape

        Returns:
            JSON response confirming the image was set
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")
        if not image_url:
            raise ValueError("Image URL cannot be empty")

        payload = {"url": image_url}

        logger.info({"message": "Scraping recipe image from URL", "slug": slug, "url": image_url})
        return self._handle_request("POST", f"/api/recipes/{slug}/image", json=payload)

    def upload_recipe_image(self, slug: str, image_data: bytes, filename: str) -> Dict[str, Any]:
        """Upload a recipe image file (multipart upload)

        Args:
            slug: The slug identifier of the recipe
            image_data: Binary image data
            filename: Name of the image file

        Returns:
            JSON response confirming the image was uploaded
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")
        if not image_data:
            raise ValueError("Image data cannot be empty")
        if not filename:
            raise ValueError("Filename cannot be empty")

        files = {"image": (filename, image_data)}

        logger.info({"message": "Uploading recipe image", "slug": slug, "filename": filename})
        return self._handle_request("PUT", f"/api/recipes/{slug}/image", files=files)

    def upload_recipe_asset(
        self, slug: str, asset_data: bytes, filename: str,
        name: str, icon: str, extension: str,
    ) -> Dict[str, Any]:
        """Upload a recipe asset file (multipart upload)

        Args:
            slug: The slug identifier of the recipe
            asset_data: Binary asset data
            filename: Name of the asset file
            name: Display name for the asset
            icon: Icon identifier for the asset (e.g., "mdi-file-pdf-box")
            extension: File extension (e.g., "pdf", "txt")

        Returns:
            JSON response containing the uploaded asset details
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")
        if not asset_data:
            raise ValueError("Asset data cannot be empty")
        if not filename:
            raise ValueError("Filename cannot be empty")

        files = {"file": (filename, asset_data)}
        data = {"name": name, "icon": icon, "extension": extension}

        logger.info({"message": "Uploading recipe asset", "slug": slug, "filename": filename})
        return self._handle_request("POST", f"/api/recipes/{slug}/assets", files=files, data=data)

    def create_recipe_from_url(
        self, url: str,
        include_tags: Optional[bool] = None,
        include_categories: Optional[bool] = None,
    ) -> str:
        """Create a new recipe by scraping a URL.

        Args:
            url: URL of the recipe to scrape
            include_tags: Whether to include tags from the scraped recipe
            include_categories: Whether to include categories from the scraped recipe

        Returns:
            Slug of the newly created recipe
        """
        if not url:
            raise ValueError("URL cannot be empty")

        payload = {"url": url}
        if include_tags is not None:
            payload["includeTags"] = include_tags
        if include_categories is not None:
            payload["includeCategories"] = include_categories

        logger.info({"message": "Creating recipe from URL", "url": url})
        return self._handle_request("POST", "/api/recipes/create/url", json=payload)

    def create_recipes_from_url_bulk(self, imports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create multiple recipes by scraping URLs.

        Args:
            imports: List of import objects, each containing 'url' and optionally 'includeTags', 'includeCategories'

        Returns:
            JSON response with import results
        """
        if not imports:
            raise ValueError("Imports list cannot be empty")

        payload = {"imports": imports}

        logger.info({"message": "Creating recipes from URLs in bulk", "count": len(imports)})
        return self._handle_request("POST", "/api/recipes/create/url/bulk", json=payload)

    def test_scrape_url(self, url: str, use_openai: Optional[bool] = None) -> Dict[str, Any]:
        """Test scraping a URL without creating a recipe.

        Args:
            url: URL to test scraping
            use_openai: Whether to use OpenAI for enhanced scraping

        Returns:
            JSON response with scraped recipe data
        """
        if not url:
            raise ValueError("URL cannot be empty")

        payload = {"url": url}
        if use_openai is not None:
            payload["useOpenAI"] = use_openai

        logger.info({"message": "Test scraping URL", "url": url})
        return self._handle_request("POST", "/api/recipes/test-scrape-url", json=payload)

    def get_recipe_suggestions(
        self,
        foods: Optional[List[str]] = None,
        tools: Optional[List[str]] = None,
        limit: Optional[int] = None,
        max_missing_foods: Optional[int] = None,
        max_missing_tools: Optional[int] = None,
        include_foods_on_hand: Optional[bool] = None,
        include_tools_on_hand: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """Get recipe suggestions based on available foods and tools.

        Args:
            foods: List of food IDs available
            tools: List of tool IDs available
            limit: Maximum number of suggestions to return
            max_missing_foods: Maximum number of missing foods allowed
            max_missing_tools: Maximum number of missing tools allowed
            include_foods_on_hand: Include foods marked as on-hand
            include_tools_on_hand: Include tools marked as on-hand

        Returns:
            List of suggested recipes
        """
        param_dict = {
            "foods": foods,
            "tools": tools,
            "limit": limit,
            "maxMissingFoods": max_missing_foods,
            "maxMissingTools": max_missing_tools,
            "includeFoodsOnHand": include_foods_on_hand,
            "includeToolsOnHand": include_tools_on_hand,
        }

        params = format_api_params(param_dict)

        logger.info({"message": "Getting recipe suggestions", "parameters": params})
        return self._handle_request("GET", "/api/recipes/suggestions", params=params)

    def delete_recipe(self, slug: str) -> Dict[str, Any]:
        """Delete a recipe

        Args:
            slug: The slug identifier of the recipe to delete

        Returns:
            JSON response confirming deletion
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")

        logger.info({"message": "Deleting recipe", "slug": slug})
        return self._handle_request("DELETE", f"/api/recipes/{slug}")
