from flask_restful import Resource, marshal_with, fields, reqparse
from app.libs.error import ParameterException, NotFound
from app.libs.fields import meta_fields
from app.libs.token_auth import auth, admin_only
from app.models.problem import Problem

create_problem_parser = reqparse.RequestParser()
create_problem_parser.add_argument('remote_oj', type=str, required=True)
create_problem_parser.add_argument('remote_prob', type=str, required=True)
create_problem_parser.add_argument('title', type=str)
create_problem_parser.add_argument('description', type=str)

modify_problem_parser = reqparse.RequestParser()
modify_problem_parser.add_argument('title', type=str)
modify_problem_parser.add_argument('description', type=str)

search_problem_parser = reqparse.RequestParser()
search_problem_parser.add_argument('remote_oj', type=str)
search_problem_parser.add_argument('remote_prob', type=str)
search_problem_parser.add_argument('title', type=str)
search_problem_parser.add_argument('description', type=str)

problem_fields = {
    'id': fields.Integer,
    'remote_oj': fields.String,
    'remote_prob': fields.String,
    'title': fields.String
}

problem_description_fields = problem_fields.copy()
problem_description_fields['description'] = fields.String

problem_list_fields = {
    'data': fields.List(fields.Nested(problem_fields)),
    'meta': fields.Nested(meta_fields)
}


class ProblemResource(Resource):
    @auth.login_required
    @admin_only
    def patch(self, id_):
        problem = Problem.get_by_id(id_)
        if not problem:
            raise NotFound()
        problem.modify(**modify_problem_parser.parse_args())
        return {'message': 'modify success'}

    @auth.login_required
    @admin_only
    def delete(self, id_):
        problem = Problem.get_by_id(id_)
        if not problem:
            raise NotFound()
        problem.delete()
        return {'message': 'delete success'}, 204


class ProblemDescriptionResource(Resource):
    @auth.login_required
    @marshal_with(problem_description_fields)
    def get(self, id_):
        problem = Problem.get_by_id(id_)
        if problem is None:
            raise NotFound()
        return problem


class ProblemCollectionResource(Resource):
    @auth.login_required
    @admin_only
    def post(self):
        args = create_problem_parser.parse_args()
        if Problem.search(remote_oj=args['remote_oj'], remote_prob=args['remote_prob'])['data']:
            raise ParameterException('problem already exist')
        problem = Problem.create(**args)
        return {'message': 'create success', 'problem_id': problem.id}, 201


class ProblemSearchResource(Resource):
    @marshal_with(problem_list_fields)
    def post(self):
        return Problem.search(**search_problem_parser.parse_args())
