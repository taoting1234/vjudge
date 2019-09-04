import re
from app.models.remote_user import RemoteUser
from app.spiders.helper import get_md5
from app.spiders.oj_spider import OjSpider
from bs4 import BeautifulSoup


class ZuccSpider(OjSpider):
    def check_login_status(self):
        url = 'http://acm.zucc.edu.cn/template/bs3/profile.php'
        res = self.request.get(url=url)
        return 'Login' not in res.text

    def login(self):
        url = 'http://acm.zucc.edu.cn/login.php'
        data = {
            'user_id': self.username,
            'password': get_md5(self.password)
        }
        res = self.request.post(url=url, data=data)
        info = re.findall(r'alert\(\'(.*)\'\);', res.text)
        if info:
            return False
        return True

    def get_status(self, remote_id):
        url = 'http://acm.zucc.edu.cn/status-ajax.php?solution_id={}'.format(remote_id)
        res = self.request.get(url=url)
        data = res.text.split(',')
        if len(data) != 5:
            return {
                'success': False
            }
        status = int(data[0])
        processing = True
        additional_info = ''
        if status == 0:
            status = 'waiting'
        elif status == 1:
            status = 'waiting rejudge'
        elif status == 2:
            status = 'compiling'
        elif status == 3:
            status = 'running'
        elif status == 4:
            status = 'accepted'
            processing = False
        elif status == 5:
            status = 'presentation error'
            processing = False
        elif status == 6:
            status = 'wrong answer'
            processing = False
        elif status == 7:
            status = 'time limit exceed'
            processing = False
        elif status == 8:
            status = 'memory limit exceed'
            processing = False
        elif status == 9:
            status = 'output limit exceed'
            processing = False
        elif status == 11:
            status = 'compile error'
            processing = False
            additional_info = self._get_ce_info(remote_id)

        time = int(data[1])
        memory = int(data[2])
        return {
            'success': True,
            'status': status,
            'time': time,
            'memory': memory,
            'processing': processing,
            'additional_info': additional_info
        }

    def submit(self, remote_oj, remote_problem, language, code, **kwargs):
        url = 'http://acm.zucc.edu.cn/submit.php?ajax'
        data = {
            'id': remote_problem,
            'language': language,
            'source': code
        }
        res = self.request.post(url=url, data=data)
        return {
            'success': True,
            'remote_id': res.text
        }

    def _get_ce_info(self, remote_id):
        url = 'http://acm.zucc.edu.cn/ceinfo.php?sid={}'.format(remote_id)
        res = self.request.get(url=url)
        soup = BeautifulSoup(res.text, 'lxml')
        try:
            return soup.find(id='errtxt').text
        except:
            return ''


if __name__ == '__main__':
    from app import create_app

    create_app().app_context().push()
    remote_user = RemoteUser.get_by_id(2)

    spider = ZuccSpider(remote_user)
    spider._get_ce_info('99839')
