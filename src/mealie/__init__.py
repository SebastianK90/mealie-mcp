from .categories import CategoriesMixin
from .client import MealieClient
from .comments import CommentsMixin
from .cookbooks import CookbooksMixin
from .foods import FoodsMixin
from .group import GroupMixin
from .labels import LabelsMixin
from .mealplan import MealplanMixin
from .organizer_tools import OrganizerToolsMixin
from .parser import ParserMixin
from .recipe import RecipeMixin
from .shopping_list import ShoppingListMixin
from .tags import TagsMixin
from .units import UnitsMixin
from .user import UserMixin


class MealieFetcher(
    RecipeMixin,
    CategoriesMixin,
    TagsMixin,
    LabelsMixin,
    FoodsMixin,
    UnitsMixin,
    OrganizerToolsMixin,
    CookbooksMixin,
    CommentsMixin,
    ParserMixin,
    ShoppingListMixin,
    MealplanMixin,
    UserMixin,
    GroupMixin,
    MealieClient,
):
    pass
