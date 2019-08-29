from flask import jsonify

from app.libs.error_code import CreateSuccess, NotFound
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.solution import Solution
from app.models.solution_log import SolutionLog
from app.spiders.service import submit_code, submit_captcha
from app.validators.forms import CreateSolutionForm, SubmitCaptchaForm

api = Redprint('solution')


@api.route('/<int:id_>', methods=['GET'])
def get_solution_api(id_):
    solution = Solution.get_by_id(id_)
    if not solution:
        raise NotFound()
    return jsonify({
        'code': 0,
        'data': {
            'solution': solution
        }
    })


@api.route('/<int:id_>/log/', methods=['GET'])
def get_solution_log_api(id_):
    res = SolutionLog.search(solution_id=id_)
    return jsonify({
        'code': 0,
        'data': {
            'res': res
        }
    })


@api.route('/', methods=['POST'])
@auth.login_required
def create_solution_api():
    form = CreateSolutionForm().validate_for_api().data_
    submit_code(form['problem_id'], form['language'], form['code'])
    return CreateSuccess('submit solution success')


@api.route('/captcha/', methods=['POST'])
def submit_captcha_api():
    form = SubmitCaptchaForm().validate_for_api().data_
    submit_captcha(form['solution_id'], form['captcha'])
    return CreateSuccess('submit captcha success')
