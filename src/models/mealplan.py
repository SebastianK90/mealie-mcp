from typing import Literal, Optional

from pydantic import BaseModel

ENTRY_TYPES = Literal["breakfast", "lunch", "dinner", "side", "snack", "drink", "dessert"]


class MealPlanEntry(BaseModel):
    date: str
    recipe_id: Optional[str] = None
    title: Optional[str] = None
    entry_type: ENTRY_TYPES = "breakfast"
