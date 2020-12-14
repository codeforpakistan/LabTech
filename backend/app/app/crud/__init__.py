from .crud_item import item
from .crud_user import user
from .crud_hospital import hospital
from .crud_department import department
from .crud_survey import survey
from .crud_feeback import feedback
from .crud_submission import submission


# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
