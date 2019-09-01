from flask_restful import Resource, reqparse, marshal_with, fields

from app.libs.error import NotFound
from app.libs.fields import meta_fields
from app.models.user import User

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('id', type=str, required=True)
create_user_parser.add_argument('password', type=str, required=True)
create_user_parser.add_argument('nickname', type=str, required=True)

modify_user_parser = reqparse.RequestParser()
modify_user_parser.add_argument('password', type=str, required=True)
modify_user_parser.add_argument('nickname', type=str, required=True)

page_parser = reqparse.RequestParser()
page_parser.add_argument('page', type=int)
page_parser.add_argument('page_size', type=int)

user_fields = {
    'id': fields.String,
    'nickname': fields.String,
    'permission': fields.Integer
}

user_data_fields = {
    'data': fields.List(fields.Nested(user_fields)),
    'meta': fields.Nested(meta_fields)
}


class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, id_):
        user = User.get_by_id(id_)
        if user is None:
            raise NotFound()
        return user

    def patch(self, id_):
        user = User.get_by_id(id_)
        if user is None:
            raise NotFound()
        user.modify(**modify_user_parser.parse_args())
        return {'message': 'modify success'}


class UserCollectionResource(Resource):
    @marshal_with(user_data_fields)
    def get(self):
        return User.search(**page_parser.parse_args())

    def post(self):
        User.create(**create_user_parser.parse_args())
        return {'message': 'create success'}, 201
