from flask import Blueprint
from flask_restful import Api

from app.api.v1.language import LanguageResource
from app.api.v1.session import SessionResource
from app.api.v1.solution import SolutionResource, SolutionCollectionResource
from app.api.v1.user import UserResource, UserCollectionResource, UserSearchResource

bp_v1 = Blueprint('v1', __name__, url_prefix='/v1')
api = Api(bp_v1, catch_all_404s=True)

# user
api.add_resource(UserResource, '/user/<int:id_>')
api.add_resource(UserCollectionResource, '/user')
api.add_resource(UserSearchResource, '/user/search')

# session
api.add_resource(SessionResource, '/session')

# language
api.add_resource(LanguageResource, '/language')

# solution
api.add_resource(SolutionResource, '/solution/<int:id_>')
api.add_resource(SolutionCollectionResource, '/solution')
