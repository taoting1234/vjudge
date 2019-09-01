from flask import Blueprint
from flask_restful import Api

from app.api.v1.session import SessionResource
from app.api.v1.user import UserResource, UserCollectionResource

bp_v1 = Blueprint('v1', __name__, url_prefix='/v1')
api = Api(bp_v1, catch_all_404s=True)

# user
api.add_resource(UserResource, '/user/<int:id_>')
api.add_resource(UserCollectionResource, '/user')

# session
api.add_resource(SessionResource, '/session')
