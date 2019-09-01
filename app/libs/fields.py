from flask_restful import fields

meta_fields = {
    'count': fields.Integer,
    'page': fields.Integer,
    'page_size': fields.Integer,
}
