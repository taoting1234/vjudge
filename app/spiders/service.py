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
        try:
            res = spider.get_status(solution.remote_id)
        except:
            time.sleep(1)
            continue
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
    g.solution.modify(status='Local info: Waiting for assign remote user')
    oj = oj.lower()
    if not RemoteUser.search(oj=oj.lower(), page_size=100000)['data']:
        oj = 'vjudge'

    remote_user = None
    while not remote_user:
        remote_user_list = RemoteUser.search(oj=oj, status=1, page_size=100000)['data']
        if remote_user_list:
            remote_user = random.choice(remote_user_list)
        else:
            time.sleep(1)
    remote_user.modify(status=0)
    return remote_user


def submit_code(solution_id, problem_id, language, code):
    solution = Solution.get_by_id(solution_id)
    g.solution = solution
    problem = Problem.get_by_id(problem_id)
    remote_user = get_remote_user(problem.remote_oj)
    solution.modify(status='Local info: Assign remote user: {}'.format(remote_user.username),
                    remote_user_id=remote_user.id)
    spider = globals()[remote_user.oj.title() + 'Spider'](remote_user)
    solution.modify(status='Local info: Submitting')
    res = spider.submit(problem.remote_oj, problem.remote_prob, language, code)
    remote_user.modify(status=1)
    if not res.get('success'):
        solution.modify(status='Remote info: {}'.format(res.get('error')), processing=0)
        return
    remote_id = res['remote_id']
    solution.modify(status='Local info: Get remote id: {}'.format(remote_id), remote_id=remote_id)
    check_status(spider, solution)


def get_problem_info(remote_oj, remote_problem):
    oj = remote_oj.lower()
    if not RemoteUser.search(oj=oj.lower(), page_size=100000)['data']:
        oj = 'vjudge'
    remote_user = random.choice(RemoteUser.search(oj=oj, page_size=100000)['data'])
    spider = globals()[remote_user.oj.title() + 'Spider'](remote_user)
    try:
        data = spider.get_problem(remote_oj, remote_problem)
    except:
        return {
            'title': '',
            'description': ''
        }
    return data
