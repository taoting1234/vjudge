from flask_restful import Resource, marshal_with, fields, reqparse
from app.api.v1.problem import problem_fields
from app.libs.error import NotFound
from app.libs.fields import meta_fields
from app.libs.parser import search_parser
from app.libs.token_auth import auth, admin_only
from app.models.contest import Contest
from app.models.problem import Problem

contest_parser = reqparse.RequestParser()
contest_parser.add_argument('name', type=str, required=True)
contest_parser.add_argument('type', type=int, required=True)
contest_parser.add_argument('start_time', type=str)
contest_parser.add_argument('end_time', type=str)
contest_parser.add_argument('problem_list', type=list, required=True)

search_contest_parser = search_parser.copy()
search_contest_parser.add_argument('name', type=str)
search_contest_parser.add_argument('type', type=str)

contest_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.Integer,
    'start_time': fields.DateTime,
    'end_time': fields.DateTime,
    'status': fields.Integer
}

contest_detail_fields = contest_fields.copy()
contest_detail_fields.update({
    'problem_list': fields.List(fields.Nested(problem_fields))
})

contest_list_fields = {
    'data': fields.List(fields.Nested(contest_fields)),
    'meta': fields.Nested(meta_fields)
}


class ContestResource(Resource):
    @marshal_with(contest_fields)
    def get(self, id_):
        contest = Contest.get_by_id(id_)
        if contest is None:
            raise NotFound()
        return contest

    @auth.login_required
    @admin_only
    def patch(self, id_):
        contest = Contest.get_by_id(id_)
        if contest is None:
            raise NotFound()
        args = contest_parser.parse_args()
        problem_list = args['problem_list']
        for problem_id in problem_list:
            problem = Problem.get_by_id(problem_id)
            if not problem:
                raise NotFound('problem {} not found'.format(problem_id))
        contest.modify(**contest_parser.parse_args())
        return {'message': 'modify success'}


class ContestDetailResource(Resource):
    @marshal_with(contest_detail_fields)
    def get(self, id_):
        contest = Contest.get_by_id(id_)
        if contest is None:
            raise NotFound()
        return contest


class ContestCollectionResource(Resource):
    @auth.login_required
    @admin_only
    def post(self):
        args = contest_parser.parse_args()
        problem_list = args['problem_list']
        for problem_id in problem_list:
            problem = Problem.get_by_id(problem_id)
            if not problem:
                raise NotFound('problem {} not found'.format(problem_id))
        Contest.modify(**contest_parser.parse_args())
        return {'message': 'create success'}, 201


class ContestSearchResource(Resource):
    @marshal_with(contest_list_fields)
    def post(self):
        return Contest.search(**search_contest_parser.parse_args())
