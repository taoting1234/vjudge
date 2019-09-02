from flask_restful import Resource, reqparse, marshal_with, fields
from app.libs.error import NotFound, AuthFailed
from app.libs.fields import meta_fields
from app.libs.parser import search_parser
from app.libs.token_auth import auth, self_only
from app.models.user import User

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('id', type=str, required=True)
create_user_parser.add_argument('password', type=str, required=True)

modify_user_parser = reqparse.RequestParser()
modify_user_parser.add_argument('old_password', type=str)
modify_user_parser.add_argument('password', type=str, required=True)
modify_user_parser.add_argument('nickname', type=str, required=True)

search_user_parser = search_parser.copy()
search_user_parser.add_argument('id', type=str)
search_user_parser.add_argument('nickname', type=str)

user_fields = {
    'id': fields.String,
    'nickname': fields.String,
    'permission': fields.Integer
}

user_list_fields = {
    'data': fields.List(fields.Nested(user_fields)),
    'meta': fields.Nested(meta_fields)
}


class UserResource(Resource):
    @auth.login_required
    @self_only
    @marshal_with(user_fields)
    def get(self, id_):
        user = User.get_by_id(id_)
        if user is None:
            raise NotFound()
        return user

    @auth.login_required
    @self_only
    def patch(self, id_):
        user = User.get_by_id(id_)
        if user is None:
            raise NotFound()
        args = modify_user_parser.parse_args()
        if args.get('password'):
            if user.check_password(args.get('old_password', '')) is False:
                raise AuthFailed('old password wrong')
        user.modify(**modify_user_parser.parse_args())
        return {'message': 'modify success'}


class UserCollectionResource(Resource):
    def post(self):
        User.create(**create_user_parser.parse_args())
        return {'message': 'create success'}, 201


class UserSearchResource(Resource):
    @marshal_with(user_list_fields)
    def post(self):
        return User.search(**search_user_parser.parse_args())
