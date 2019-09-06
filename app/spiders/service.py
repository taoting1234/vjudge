import random
import time

from flask import g

from app.models.problem import Problem
from app.models.remote_user import RemoteUser
from threading import Thread
# 导入spider
from app.models.solution import Solution
from app.spiders.vjudge_spider import VjudgeSpider
from app.spiders.zucc_spider import ZuccSpider


def async_submit_code(problem_id, solution_id, language, code):
    t = Thread(target=submit_code_with_context, args=(problem_id, solution_id, language, code))
    t.start()


def submit_code_with_context(problem_id, solution_id, language, code):
    from app import create_app
    with create_app().app_context():
        submit_code(problem_id, solution_id, language, code)


def check_status(spider, solution):
    last_status = None
    t = 0
    while 1:
        t += 1
        res = spider.get_status(solution.remote_id)
        now_status = 'Remote info: {}'.format(res.get('status'))
        res['status'] = now_status
        if last_status != now_status:
            solution.modify(**res)
            last_status = now_status
        if not res['processing']:
            break
        if t >= 100:
            solution.modify(status='Local info: Get status timeout, break', processing=0)
            break
        time.sleep(1)


def get_remote_user(oj):
    remote_user_list = RemoteUser.search(oj=oj.lower(), status=1, page_size=100000)['data']
    if remote_user_list:
        remote_user = random.choice(remote_user_list)
    else:
        remote_user = random.choice(RemoteUser.search(oj='vjudge', status=1, page_size=100000)['data'])
    return remote_user


def submit_code(solution_id, problem_id, language, code):
    problem = Problem.get_by_id(problem_id)
    remote_user = get_remote_user(problem.remote_oj)
    solution = Solution.get_by_id(solution_id)
    solution.modify(status='Local info: Assign remote user: {}'.format(remote_user.username),
                    remote_user_id=remote_user.id)
    spider = globals()[remote_user.oj.title() + 'Spider'](remote_user)
    solution.modify(status='Local info: Submitting')
    g.solution = solution
    res = spider.submit(problem.remote_oj, problem.remote_prob, language, code)
    if not res.get('success'):
        solution.modify(status='Remote info: {}'.format(res.get('error')))
        return
    remote_id = res['remote_id']
    solution.modify(status='Local info: Get remote id: {}'.format(remote_id), remote_id=remote_id)
    check_status(spider, solution)
