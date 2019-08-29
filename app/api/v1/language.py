from flask import jsonify
from app.libs.redprint import Redprint
from app.models.language import Language

api = Redprint('language')


@api.route('/', methods=['GET'])
def get_language_api():
    res = Language.search()
    return jsonify({
        'code': 0,
        'data': {
            'res': res
        }
    })
