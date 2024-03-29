from flask_restful import Resource, marshal_with, fields, reqparse
from app.libs.error import ParameterException, NotFound, Forbidden
from app.libs.fields import meta_fields
from app.libs.token_auth import auth, admin_only, get_current_user
from app.models.problem import Problem
from app.spiders.service import get_problem_info

create_problem_parser = reqparse.RequestParser()
create_problem_parser.add_argument('remote_oj', type=str, required=True)
create_problem_parser.add_argument('remote_prob', type=str, required=True)

modify_problem_parser = reqparse.RequestParser()
modify_problem_parser.add_argument('title', type=str)
modify_problem_parser.add_argument('description', type=str)
modify_problem_parser.add_argument('status', type=int)

search_problem_parser = reqparse.RequestParser()
search_problem_parser.add_argument('remote_oj', type=str)
search_problem_parser.add_argument('remote_prob', type=str)
search_problem_parser.add_argument('title', type=str)
search_problem_parser.add_argument('status', type=int)

problem_fields = {
    'id': fields.Integer,
    'remote_oj': fields.String,
    'remote_prob': fields.String,
    'title': fields.String,
    'accept_number': fields.Integer,
    'submit_number': fields.Integer,
    'status': fields.Integer
}

problem_detail_fields = problem_fields.copy()
problem_detail_fields.update({
    'description': fields.String
})

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


class ProblemDetailResource(Resource):
    @auth.login_required
    @marshal_with(problem_detail_fields)
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
        data = get_problem_info(args['remote_oj'], args['remote_prob'])
        problem = Problem.create(**args, title=data['title'], description=data['description'], status=0)
        return {'message': 'create success', 'problem_id': problem.id}, 201


class ProblemSearchResource(Resource):
    @marshal_with(problem_list_fields)
    def post(self):
        args = search_problem_parser.parse_args()
        user = get_current_user()
        if args['status']:
            if not user or user.permission != -1:
                raise Forbidden()
        return Problem.search(**args)
