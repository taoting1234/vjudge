from flask import g
from flask_restful import Resource, reqparse, marshal_with
from app.api.v1.user import user_fields
from app.config.setting import TOKEN_EXPIRATION
from app.libs.token_auth import auth, generate_auth_token
from app.models.user import User

login_parser = reqparse.RequestParser()
login_parser.add_argument('id_', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)


class SessionResource(Resource):
    @auth.login_required
    @marshal_with(user_fields)
    def get(self):
        return g.user

    def post(self):
        identity = User.verify(**login_parser.parse_args())
        token = generate_auth_token(identity['uid'], TOKEN_EXPIRATION)
        return {'token': token}

    @auth.login_required
    def put(self):
        token = generate_auth_token(g.user.id, TOKEN_EXPIRATION)
        return {'token': token}

    @auth.login_required
    def delete(self):
        return {'message': 'delete success'}, 204
