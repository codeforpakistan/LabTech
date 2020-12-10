# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.item import Item  # noqa
from app.models.user import User  # noqa
from app.models.hospital import Hospital
from app.models.department import Department
from app.models.survey import Survey
from app.models.feedback import Feedback
from app.models.submission import Submission
