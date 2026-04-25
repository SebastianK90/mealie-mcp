# Mealie MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server for [Mealie](https://mealie.io/) -- the self-hosted recipe manager and meal planner. Gives LLMs full access to manage recipes, meal plans, shopping lists, and more through your Mealie instance.

## Tools

### Recipes
| Tool | Description |
|------|-------------|
| `get_recipes` | Search and list recipes with filtering by categories, tags, tools, and advanced query filters |
| `get_recipe_detailed` | Get full recipe details including ingredients, instructions, and metadata |
| `get_recipe_concise` | Get a summary of a recipe (name, servings, time, ingredients, rating) |
| `create_recipe` | Create a new recipe with name, ingredients, and instructions |
| `update_recipe` | Replace the ingredients and instructions of an existing recipe |
| `patch_recipe` | Partially update recipe metadata (name, description, times, servings, rating, etc.) |
| `duplicate_recipe` | Duplicate an existing recipe |
| `delete_recipe` | Delete a recipe permanently |
| `mark_recipe_last_made` | Mark a recipe as made today |
| `get_recipe_suggestions` | Get recipe suggestions based on available foods and tools on hand |
| `create_recipe_from_url` | Import a recipe by scraping it from a URL |
| `create_recipes_from_url_bulk` | Import multiple recipes from URLs at once |
| `test_scrape_url` | Preview scraped recipe data from a URL without saving |
| `set_recipe_image_from_url` | Set a recipe's image by scraping it from a URL |
| `upload_recipe_image_file` | Upload a local image file for a recipe |
| `upload_recipe_asset_file` | Upload a document/asset file for a recipe |

### Meal Plans
| Tool | Description |
|------|-------------|
| `get_all_mealplans` | Get meal plans with optional date range filtering |
| `get_todays_mealplan` | Get today's meal plan entries |
| `get_mealplan` | Get a specific meal plan entry by ID |
| `create_mealplan` | Create a meal plan entry (breakfast, lunch, dinner, side, snack, drink, dessert) |
| `create_mealplan_bulk` | Create multiple meal plan entries at once |
| `create_random_mealplan` | Create a meal plan entry with a randomly selected recipe |
| `update_mealplan` | Update a meal plan entry |
| `delete_mealplan` | Delete a meal plan entry |

### Shopping Lists
| Tool | Description |
|------|-------------|
| `get_shopping_lists` | Get all shopping lists |
| `get_shopping_list` | Get a specific shopping list with all items |
| `create_shopping_list` | Create a new shopping list |
| `delete_shopping_list` | Delete a shopping list |
| `add_recipe_to_shopping_list` | Add a recipe's ingredients to a shopping list |
| `remove_recipe_from_shopping_list` | Remove a recipe's ingredients from a shopping list |

### Shopping List Items
| Tool | Description |
|------|-------------|
| `get_shopping_list_items` | Get all shopping list items with search and pagination |
| `get_shopping_list_item` | Get a specific shopping list item |
| `create_shopping_list_item` | Create a new item in a shopping list |
| `create_shopping_list_items_bulk` | Create multiple shopping list items at once |
| `update_shopping_list_item` | Update a shopping list item (check/uncheck, modify, assign label) |
| `update_shopping_list_items_bulk` | Update multiple shopping list items at once |
| `delete_shopping_list_item` | Delete a shopping list item |
| `delete_shopping_list_items_bulk` | Delete multiple shopping list items at once |

### Categories
| Tool | Description |
|------|-------------|
| `get_categories` | Get all recipe categories |
| `get_category` | Get a category by ID |
| `get_category_by_slug` | Get a category by slug |
| `get_empty_categories` | Get categories with no recipes |
| `create_category` | Create a new category |
| `update_category` | Update a category |
| `delete_category` | Delete a category |

### Tags
| Tool | Description |
|------|-------------|
| `get_tags` | Get all recipe tags |
| `get_tag` | Get a tag by ID |
| `get_tag_by_slug` | Get a tag by slug |
| `get_empty_tags` | Get tags with no recipes |
| `create_tag` | Create a new tag |
| `update_tag` | Update a tag |
| `delete_tag` | Delete a tag |

### Foods
| Tool | Description |
|------|-------------|
| `get_foods` | Get all foods (ingredients in the database) |
| `get_food` | Get a specific food by ID |
| `create_food` | Create a new food |
| `update_food` | Update a food's details |
| `delete_food` | Delete a food |
| `merge_foods` | Merge one food into another (updates all references) |

### Units
| Tool | Description |
|------|-------------|
| `get_units` | Get all measurement units |
| `get_unit` | Get a specific unit by ID |
| `create_unit` | Create a new unit |
| `update_unit` | Update a unit's details |
| `delete_unit` | Delete a unit |
| `merge_units` | Merge one unit into another (updates all references) |

### Tools (Kitchen Equipment)
| Tool | Description |
|------|-------------|
| `get_tools` | Get all kitchen tools/equipment |
| `get_tool` | Get a tool by ID |
| `get_tool_by_slug` | Get a tool by slug |
| `create_tool` | Create a new tool |
| `update_tool` | Update a tool |
| `delete_tool` | Delete a tool |

### Labels
| Tool | Description |
|------|-------------|
| `get_labels` | Get all multi-purpose labels (for shopping list item categorization) |
| `get_label` | Get a label by ID |
| `create_label` | Create a new label |
| `update_label` | Update a label's name or color |
| `delete_label` | Delete a label |

### Cookbooks
| Tool | Description |
|------|-------------|
| `get_cookbooks` | Get all cookbooks (curated recipe collections) |
| `get_cookbook` | Get a cookbook by ID |
| `create_cookbook` | Create a new cookbook with optional query filter |
| `update_cookbook` | Update a cookbook |
| `delete_cookbook` | Delete a cookbook |

### Comments
| Tool | Description |
|------|-------------|
| `get_recipe_comments` | Get all comments on a recipe |
| `create_comment` | Add a comment to a recipe |
| `update_comment` | Update a comment |
| `delete_comment` | Delete a comment |

### Ingredient Parser
| Tool | Description |
|------|-------------|
| `parse_ingredient` | Parse a single ingredient string into structured data (quantity, unit, food) |
| `parse_ingredients` | Parse multiple ingredient strings at once |

### User & Household
| Tool | Description |
|------|-------------|
| `get_current_user` | Get the current user's profile info |
| `get_user_favorites` | Get the current user's favorite recipes |
| `get_user_ratings` | Get the current user's recipe ratings |
| `add_favorite` | Add a recipe to favorites |
| `remove_favorite` | Remove a recipe from favorites |
| `set_recipe_rating` | Rate a recipe (0-5) and/or set favorite status |
| `get_household_statistics` | Get household stats (total recipes, categories, tags, etc.) |

## Prompts

| Prompt | Description |
|--------|-------------|
| `weekly_meal_plan` | Interactive weekly meal planning workflow that searches your recipes and builds a balanced 7-day plan |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MEALIE_BASE_URL` | Yes | Base URL of your Mealie instance (e.g., `https://mealie.example.com`) |
| `MEALIE_API_KEY` | Yes | API key for authenticating with Mealie (generate in Mealie under User > API Tokens) |
| `LOG_LEVEL` | No | Logging level (default: `INFO`) |
| `MCP_TRANSPORT` | No | Transport mode: `stdio` (default) or `sse` |

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
# Clone the repo
git clone https://github.com/GraysonCAdams/mealie-mcp.git
cd mealie-mcp

# Install dependencies
uv sync

# Set environment variables
export MEALIE_BASE_URL="https://mealie.example.com"
export MEALIE_API_KEY="your-api-key-here"
```

Or create a `.env` file in the project root:

```env
MEALIE_BASE_URL=https://mealie.example.com
MEALIE_API_KEY=your-api-key-here
```

## Running

### stdio mode (for direct MCP client connections)

```bash
uv run src/server.py
```

### HTTP mode with mcp-proxy

```bash
mcp-proxy --port 8004 -- uv run src/server.py
```

### Gemini CLI configuration

Add to your Gemini CLI config (`.gemini/settings.json`):

```json
{
  "mcpServers": {
    "mealie": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mealie-mcp", "src/server.py"],
      "env": {
        "MEALIE_BASE_URL": "https://mealie.example.com",
        "MEALIE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Claude Desktop configuration

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mealie": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mealie-mcp", "src/server.py"],
      "env": {
        "MEALIE_BASE_URL": "https://mealie.example.com",
        "MEALIE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## License

MIT
