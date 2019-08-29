from flask import jsonify
from app.libs.redprint import Redprint
from app.models.problem import Problem

api = Redprint('problem')


@api.route('/<int:id_>', methods=['GET'])
def get_problem_api(id_):
    problem = Problem.get_by_id(id_)
    if not problem:
        raise problem()
    return jsonify({
        'code': 0,
        'data': {
            'problem': problem
        }
    })

