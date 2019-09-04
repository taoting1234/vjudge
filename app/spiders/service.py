import random
import time
from flask import g
from app.models.problem import Problem
from app.models.remote_user import RemoteUser
from app.models.solution import Solution
from app.models.solution_log import SolutionLog
# 导入spider
from app.spiders.vjudge_spider import VjudgeSpider
from app.spiders.zucc_spider import ZuccSpider


def check_status(spider, solution):
    last_status = None
    t = 0
    while 1:
        t += 1
        res = spider.get_status(solution.remote_id)
        now_status = res.get('status')
        additional_info = res.get('additional_info')
        if last_status != now_status:
            SolutionLog.create(solution_id=solution.id, status=now_status)
            last_status = now_status
        if additional_info:
            solution.modify(additional_info=additional_info)
        if not res.get('processing') or t >= 100:
            solution.modify(processing=0)
            break
        time.sleep(1)


def get_remote_user(oj):
    remote_user_list = RemoteUser.search(oj=oj.lower(), page_size=100000)['data']
    if remote_user_list:
        remote_user = random.choice(remote_user_list)
    else:
        remote_user = random.choice(RemoteUser.search(oj='vjudge', page_size=100000)['data'])
    return remote_user


def submit_code(problem_id, solution_id, language, code):
    problem = Problem.get_by_id(problem_id)
    solution = Solution.get_by_id(solution_id)
    remote_user = get_remote_user(problem.remote_oj)
    solution.modify(remote_user_id=remote_user.id)
    SolutionLog.create(solution_id=solution.id, status='create solution')
    spider = globals()[remote_user.oj.title() + 'Spider'](remote_user)
    res = spider.submit(problem.remote_oj, problem.remote_prob, language, code)
    if not res.get('success'):
        SolutionLog.create(solution_id=solution.id, status=res.get('error'))
        return
    remote_id = res.get('remote_id')
    SolutionLog.create(solution_id=solution.id, status='get remote id success')
    solution.modify(remote_id=remote_id)
    if solution.remote_id:
        check_status(spider, solution)
