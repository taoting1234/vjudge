import re

from parsel import Selector

from app.models.remote_user import RemoteUser
from app.libs.helper import get_md5
from app.spiders.oj_spider import OjSpider
from bs4 import BeautifulSoup


class ZuccSpider(OjSpider):
    host = 'acm.zucc.edu.cn'

    def check_login_status(self):
        url = 'http://{}/template/bs3/profile.php'.format(self.host)
        res = self.request.get(url=url)
        return 'Login' not in res.text

    def login(self):
        url = 'http://{}/login.php'.format(self.host)
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
        url = 'http://{}/status-ajax.php?solution_id={}'.format(self.host, remote_id)
        res = self.request.get(url=url)
        data = res.text.split(',')
        if len(data) != 5:
            return {
                'success': False
            }
        status = int(data[0])
        processing = 1
        additional_info = ''
        if status == 0:
            status = 'Waiting'
        elif status == 1:
            status = 'Waiting rejudge'
        elif status == 2:
            status = 'Compiling'
        elif status == 3:
            status = 'Running'
        elif status == 4:
            status = 'Accepted'
            processing = 0
        elif status == 5:
            status = 'Presentation error'
            processing = 0
        elif status == 6:
            status = 'Wrong answer'
            processing = 0
        elif status == 7:
            status = 'Time limit exceed'
            processing = 0
        elif status == 8:
            status = 'Memory limit exceed'
            processing = 0
        elif status == 9:
            status = 'Output limit exceed'
            processing = 0
        elif status == 11:
            status = 'Compile error'
            processing = 0
            additional_info = self._get_ce_info(remote_id)

        time = int(data[2])
        memory = int(data[1])
        return {
            'success': True,
            'status': status,
            'run_time': time,
            'run_memory': memory,
            'processing': processing,
            'additional_info': additional_info
        }

    def submit(self, remote_oj, remote_problem, language, code, **kwargs):
        url = 'http://{}/submit.php?ajax'.format(self.host)
        data = {
            'id': remote_problem,
            'language': language,
            'source': code
        }
        res = self.request.post(url=url, data=data)
        try:
            int(res.text)
        except:
            return {
                'success': False,
                'error': 'Get Remote id error'
            }
        return {
            'success': True,
            'remote_id': res.text
        }

    def _get_ce_info(self, remote_id):
        url = 'http://{}/ceinfo.php?sid={}'.format(self.host, remote_id)
        res = self.request.get(url=url)
        soup = BeautifulSoup(res.text, 'lxml')
        try:
            return soup.find(id='errtxt').text
        except:
            return ''

    def get_problem(self, remote_oj, remote_problem):
        url = 'http://acm.zucc.edu.cn/problem.php?id={}'.format(remote_problem)
        res = self.request.get(url=url)
        selector = Selector(res.text)
        title = selector.xpath('/html/body/div[1]/div[2]/div[1]/center/h3/text()').get('').split(':')[1].strip()
        data = {
            'time_limit': float(
                selector.xpath('/html/body/div[1]/div[2]/div[1]/center/span[2]/span/text()').get('').strip()),
            'memory_limit': float(
                selector.xpath('/html/body/div[1]/div[2]/div[1]/center/text()[2]').get('').replace('MB', '').strip()),
            'description': selector.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/text()').get('').strip(),
            'input': selector.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/text()').get('').strip(),
            'output': selector.xpath('/html/body/div[1]/div[2]/div[2]/div[3]/div[2]/text()').get('').strip(),
            'sample_input': selector.xpath('//*[@id="sampleinput"]/text()').get('').replace('\r', '').strip(),
            'sample_output': selector.xpath('//*[@id="sampleoutput"]/text()').get('').replace('\r', '').strip()
        }
        return {
            'title': title,
            'description': self.problem_format.format(**data)
        }


if __name__ == '__main__':
    from app import create_app

    create_app().app_context().push()
    remote_user = RemoteUser.get_by_id(3)

    spider = ZuccSpider(remote_user)
    r = spider.get_problem('', '1000')
    print(r)
