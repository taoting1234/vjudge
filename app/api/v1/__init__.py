from flask import Blueprint
from flask_restful import Api

from app.api.v1.contest import ContestResource, ContestDetailResource, ContestCollectionResource, ContestSearchResource
from app.api.v1.language import LanguageResource
from app.api.v1.problem import ProblemResource, ProblemCollectionResource, ProblemSearchResource, ProblemDetailResource
from app.api.v1.session import SessionResource
from app.api.v1.solution import SolutionResource, SolutionCollectionResource, SolutionSearchResource, \
    SolutionDetailResource, SolutionRejudgeResource
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
api.add_resource(SolutionDetailResource, '/solution/<int:id_>/detail')
api.add_resource(SolutionRejudgeResource, '/solution/<int:id_>/rejudge')
api.add_resource(SolutionCollectionResource, '/solution')
api.add_resource(SolutionSearchResource, '/solution/search')

# problem
api.add_resource(ProblemResource, '/problem/<int:id_>')
api.add_resource(ProblemDetailResource, '/problem/<int:id_>/detail')
api.add_resource(ProblemCollectionResource, '/problem')
api.add_resource(ProblemSearchResource, '/problem/search')

# contest
api.add_resource(ContestResource, '/contest/<int:id>')
api.add_resource(ContestDetailResource, '/contest/<int:id>/detail')
api.add_resource(ContestCollectionResource, '/contest')
api.add_resource(ContestSearchResource, '/contest/search')
