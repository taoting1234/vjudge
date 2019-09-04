from flask_restful import Resource, marshal_with, fields
from app.libs.token_auth import auth
from app.models.language import Language

language_fields = {
    'id': fields.Integer,
    'oj': fields.String,
    'key': fields.String,
    'value': fields.String
}

language_list_fields = {
    'data': fields.List(fields.Nested(language_fields)),
}


class LanguageResource(Resource):
    @auth.login_required
    @marshal_with(language_list_fields)
    def get(self):
        return {'data': Language.search(page=1, page_size=100000)['data']}
