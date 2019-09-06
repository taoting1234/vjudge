from flask import g
from flask_restful import Resource, reqparse, marshal_with, fields
from app.libs.error import NotFound, ParameterException
from app.libs.fields import meta_fields
from app.libs.parser import search_parser
from app.libs.token_auth import auth, self_only, admin_only
from app.models.language import Language
from app.models.problem import Problem
from app.models.solution import Solution
from app.models.solution_log import SolutionLog
from app.spiders.service import async_submit_code

create_solution_parser = reqparse.RequestParser()
create_solution_parser.add_argument('problem_id', type=int, required=True)
create_solution_parser.add_argument('code', type=str, required=True)
create_solution_parser.add_argument('language', type=str, required=True)

search_solution_parser = search_parser.copy()
search_solution_parser.add_argument('problem_id', type=int)
search_solution_parser.add_argument('user_id', type=str)
search_solution_parser.add_argument('language_canonical', type=str)
search_solution_parser.add_argument('status_canonical', type=str)
search_solution_parser.add_argument('processing', type=int)

modify_solution_parser = reqparse.RequestParser()
modify_solution_parser.add_argument('status', type=str, required=True)

solution_fields = {
    'id': fields.Integer,
    'problem_id': fields.Integer,
    'user_id': fields.String,
    'language': fields.String,
    'language_canonical': fields.String,
    'status': fields.String,
    'status_canonical': fields.String,
    'processing': fields.Integer,
    'remote_id': fields.String,
    'remote_user_id': fields.Integer,
    'additional_info': fields.String,
    'create_time': fields.DateTime(dt_format='iso8601')
}

solution_code_fields = solution_fields.copy()
solution_code_fields['code'] = fields.String

solution_list_fields = {
    'data': fields.List(fields.Nested(solution_fields)),
    'meta': fields.Nested(meta_fields)
}

solution_log_fields = {
    'id': fields.Integer,
    'status': fields.String,
    'create_time': fields.DateTime('iso8601')
}

solution_log_list_fields = {
    'data': fields.List(fields.Nested(solution_log_fields)),
}


class SolutionResource(Resource):
    @auth.login_required
    @marshal_with(solution_fields)
    def get(self, id_):
        solution = Solution.get_by_id(id_)
        if solution is None:
            raise NotFound()
        return solution

    @auth.login_required
    @admin_only
    @marshal_with(solution_fields)
    def patch(self, id_):
        solution = Solution.get_by_id(id_)
        if solution is None:
            raise NotFound()
        status = modify_solution_parser.parse_args()['status']
        solution.modify(status='{} modify status to {}'.format(g.user.id, status))


class SolutionCodeResource(Resource):
    @auth.login_required
    @self_only
    @marshal_with(solution_code_fields)
    def get(self, id_):
        solution = Solution.get_by_id(id_)
        if solution is None:
            raise NotFound()
        return solution


class SolutionLogResource(Resource):
    @auth.login_required
    @self_only
    @marshal_with(solution_log_list_fields)
    def get(self, id_):
        solution_log = SolutionLog.search(solution_id=id_, page_size=100000)['data']
        return {'data': solution_log}


class SolutionCollectionResource(Resource):
    @auth.login_required
    def post(self):
        args = create_solution_parser.parse_args()
        problem = Problem.get_by_id(args['problem_id'])
        real_language = Language.search(oj=problem.remote_oj, key=args['language'])['data']
        if not real_language:
            raise ParameterException('language does not exist')
        real_language = real_language[0].value
        old_language = args['language']
        args['language'] = real_language
        solution = Solution.create(**args, user_id=g.user.id, status='create solution')
        async_submit_code(solution.id, args['problem_id'], old_language, args['code'])
        return {'message': 'create success', 'solution_id': solution.id}, 201


class SolutionSearchResource(Resource):
    @marshal_with(solution_list_fields)
    def post(self):
        return Solution.search(**search_solution_parser.parse_args())
