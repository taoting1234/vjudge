from app import create_app
from app.models.user import User

create_app().app_context().push()

user = User.get_by_id('31702411')
user.modify(password='990718')