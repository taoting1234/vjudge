from app.models.language import Language
from app.spiders.helper import get_base64
from app.spiders.oj_spider import OjSpider
from app.spiders.spider_http import SpiderHttp


class VjudgeSpider(OjSpider):
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
        for k, v in res.items():
            Language.delete_oj(v['name'])
            for key, value in v['languages'].items():
                Language.create(oj=v['name'], key=key, value=value)

    def submit(self, remote_oj, remote_problem, language, code, **kwargs):
        url = 'https://vjudge.net/problem/submit'
        data = {
            'language': language,
            'share': 0,
            'source': get_base64(code),
            'captcha': kwargs.get('captcha', ''),
            'oj': remote_oj,
            'probNum': remote_problem,
        }
        res = self.request.post(url=url, data=data).json()
        error = res.get('error')
        if error:
            if 'captcha' in error:
                pass
            return {
                'success': False,
                'error': error
            }
        return {
            'success': True,
            'remote_id': res.get('runId')
        }

    def get_status(self, remote_id):
        url = 'https://vjudge.net/solution/data/{}'.format(remote_id)
        res = self.request.post(url=url)
        return res.json()

    def _get_captcha(self):
        url = 'https://vjudge.net/util/captcha'
        res = self.request.get(url=url)
        return get_base64(res.content)


if __name__ == '__main__':
    from app import create_app

    create_app().app_context().push()

    VjudgeSpider.get_remote_oj()
