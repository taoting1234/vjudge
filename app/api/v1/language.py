from flask_restful import Resource, marshal_with, fields
from app.libs.token_auth import auth
from app.models.language import Language

value_fields = {
    fields.String: fields.String
}

language_fields = {
    'oj': fields.String,
    'data': fields.List(fields.Nested(value_fields))
}

language_list_fields = {
    'data': fields.List(fields.Nested(language_fields))
}


class LanguageResource(Resource):
    @auth.login_required
    @marshal_with(language_list_fields)
    def get(self):
        data = dict()
        for i in Language.search(page_size=100000)['data']:
            data

        return {'data': Language.search(page_size=100000)['data']}
