import random
import time
from flask import g
from app.models.language import Language
from app.models.problem import Problem
from app.models.remote_user import RemoteUser
from app.models.solution import Solution
from app.models.solution_log import SolutionLog
from app.spiders.vjudge_spider import VjudgeSpider


def check_status(solution, spider):
    last_status = None
    while 1:
        res = spider.get_status(solution.remote_id)
        now_status = res.get('status')
        additional_info = res.get('additionalInfo')
        if last_status != now_status:
            SolutionLog.create_solution_log(solution.id, now_status)
            last_status = now_status
        if additional_info:
            solution.modify(additional_info=additional_info)
        if res.get('processing') is False:
            solution.modify(processing=0)
            break
        time.sleep(1)


def get_remote_id(res, spider, solution):
    error = res.get('error')
    if error:
        if res.get('captcha'):
            captcha = spider.get_captcha()
            SolutionLog.create_solution_log(solution.id, error, captcha)
        else:
            SolutionLog.create_solution_log(solution.id, error)
        solution.modify(processing=0)
        return
    remote_id = res.get('runId')
    if not remote_id:
        SolutionLog.create_solution_log(solution.id, 'get remote id failed')
        solution.modify(processing=0)
        return
    SolutionLog.create_solution_log(solution.id, 'submit success')
    solution.modify(remote_id=remote_id)


def submit_code(problem_id, language, code):
    problem = Problem.get_by_id(problem_id)
    remote_user = random.choice(RemoteUser.search()['data'])
    real_language = Language.search(oj=problem.remote_oj, key=language)['data'][0].value
    solution = Solution.create_solution(problem_id, g.user.username, code, real_language, remote_user.id)
    SolutionLog.create_solution_log(solution.id, 'create solution')
    spider = VjudgeSpider(remote_user)
    res = spider.submit(problem.remote_oj, problem.remote_prob, language, code)
    get_remote_id(res, spider, solution)
    if solution.remote_id:
        check_status(solution, spider)


def submit_captcha(solution_id, captcha):
    solution = Solution.get_by_id(solution_id)
    remote_user = RemoteUser.get_by_id(solution.remote_user_id)
    spider = VjudgeSpider(remote_user)
    problem = Problem.get_by_id(solution.problem_id)
    language = Language.search(oj=problem.remote_oj, value=solution.language)['data'][0].key
    res = spider.submit(problem.remote_oj, problem.remote_prob, language, solution.code, captcha)
    get_remote_id(res, spider, solution)
    if solution.remote_id:
        check_status(solution, spider)
