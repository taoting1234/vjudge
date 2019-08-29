import base64

from app import create_app
from app.models.language import Language
from app.spiders.spider_http import SpiderHttp


class VjudgeSpider:
    def __init__(self, remote_user):
        self.username = remote_user.username
        self.password = remote_user.password
        self.request = SpiderHttp()
        if remote_user.cookies:
            self.request.sess.cookies.update(remote_user.cookies)

        if not self.check_login_status():
            if not self.login():
                raise Exception('remote user login error')
            assert self.check_login_status()
            remote_user.modify(cookies=self.request.sess.cookies.get_dict())

    def check_login_status(self):
        url = 'https://vjudge.net/user/checkLogInStatus'
        res = self.request.post(url=url)
        return res.text == 'true'

    def login(self):
        url = 'https://vjudge.net/user/login'
        self.request.sess.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        data = {
            'username': self.username,
            'password': self.password
        }
        res = self.request.post(url=url, data=data)
        self.request.headers.pop('Content-Type')
        return res.text == 'success'

    @staticmethod
    def get_remote_oj():
        url = 'https://vjudge.net/util/remoteOJs'
        res = SpiderHttp().get(url=url).json()
        Language.delete_all()
        for k, v in res.items():
            for key, value in v['languages'].items():
                Language.create_language(v['name'], key, value)

    def submit(self, remote_oj, remote_problem, language, code, captcha=''):
        url = 'https://vjudge.net/problem/submit'
        data = {
            'language': language,
            'share': 0,
            'source': base64.b64encode(code.encode('utf8')).decode(),
            'captcha': captcha,
            'oj': remote_oj,
            'probNum': remote_problem,
        }
        res = self.request.post(url=url, data=data)
        return res.json()

    def get_status(self, remote_id):
        url = 'https://vjudge.net/solution/data/{}'.format(remote_id)
        res = self.request.post(url=url)
        return res.json()

    def get_captcha(self):
        url = 'https://vjudge.net/util/captcha'
        res = self.request.get(url=url)
        return base64.b64encode(res.content).decode()


if __name__ == '__main__':
    create_app().app_context().push()

    VjudgeSpider.get_remote_oj()
