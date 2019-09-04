from flask import Blueprint
from flask_restful import Api

from app.api.v1.language import LanguageResource
from app.api.v1.problem import ProblemResource, ProblemDescriptionResource, ProblemCollectionResource, \
    ProblemSearchResource
from app.api.v1.session import SessionResource
from app.api.v1.solution import SolutionResource, SolutionCollectionResource, SolutionCodeResource, \
    SolutionSearchResource, SolutionLogResource
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
api.add_resource(SolutionCodeResource, '/solution/<int:id_>/code')
api.add_resource(SolutionLogResource, '/solution/<int:id_>/log')
api.add_resource(SolutionCollectionResource, '/solution')
api.add_resource(SolutionSearchResource, '/solution/search')

# problem
api.add_resource(ProblemResource, '/problem/<int:id_>')
api.add_resource(ProblemDescriptionResource, '/problem/<int:id_>/description')
api.add_resource(ProblemCollectionResource, '/problem')
api.add_resource(ProblemSearchResource, '/problem/search')
