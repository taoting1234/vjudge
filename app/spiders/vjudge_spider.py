from urllib.parse import quote
from flask import g
from app.models.language import Language
from app.spiders.captcha import Lianzhong, save_captcha
from app.libs.helper import get_base64
from app.spiders.oj_spider import OjSpider
from app.spiders.spider_http import SpiderHttp


class VjudgeSpider(OjSpider):
    host = 'cn.vjudge.net'

    def check_login_status(self):
        url = 'https://{}/user/checkLogInStatus'.format(self.host)
        res = self.request.post(url=url)
        return res.text == 'true'

    def login(self):
        url = 'https://{}/user/login'.format(self.host)
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

    @classmethod
    def get_remote_oj(cls):
        url = 'https://{}/util/remoteOJs'.format(cls.host)
        res = SpiderHttp().get(url=url).json()
        for k, v in res.items():
            Language.delete_oj(v['name'])
            for key, value in v['languages'].items():
                Language.create(oj=v['name'], key=key, value=value)

    def submit(self, remote_oj, remote_problem, language, code, **kwargs):
        url = 'https://{}/problem/submit'.format(self.host)
        data = {
            'language': language,
            'share': 0,
            'source': get_base64(quote(code)),
            'captcha': kwargs.get('captcha_result', ''),
            'oj': remote_oj,
            'probNum': remote_problem,
        }
        res = self.request.post(url=url, data=data).json()
        error = res.get('error')
        if error:
            g.solution.modify(status='Remote info: {}'.format(error))
            if 'Captcha' in error:
                if kwargs.get('captcha_id'):
                    Lianzhong.report(kwargs.get('captcha_id'))
                captcha = self._get_captcha()
                g.solution.modify(status='Local info: Try to recognize captcha')
                captcha_res = Lianzhong.recognize(captcha)
                if not captcha_res.get('success'):
                    return {
                        'success': False,
                        'error': 'recognize error: {}'.format(captcha_res.get('message'))
                    }
                captcha_id = captcha_res['captcha_id']
                captcha_result = captcha_res['result']
                g.solution.modify(status='Local info: Recognize captcha success: {}'.format(captcha_result))
                g.solution.modify(status='Local info: Resubmitting')
                return self.submit(remote_oj, remote_problem, language, code,
                                   captcha_id=captcha_id, captcha_result=captcha_result, captcha=captcha)
            return {
                'success': False,
                'error': error
            }
        if kwargs.get('captcha_result'):
            save_captcha(kwargs.get('captcha'), kwargs.get('captcha_result'))
        try:
            return {
                'success': True,
                'remote_id': res.get('runId')
            }
        except:
            return {
                'success': False,
                'error': 'Get remote id error'
            }

    def get_status(self, remote_id):
        url = 'https://{}/solution/data/{}'.format(self.host, remote_id)
        res = self.request.post(url=url).json()

        return {
            'success': True,
            'status': res['status'],
            'run_time': res.get('runtime', 0),
            'run_memory': res.get('memory', 0),
            'processing': res['processing'] is True,
            'additional_info': res.get('additionalInfo'),
        }

    def _get_captcha(self):
        url = 'https://{}/util/captcha'.format(self.host)
        res = self.request.get(url=url)
        return res.content


if __name__ == '__main__':
    from app import create_app

    create_app().app_context().push()

    VjudgeSpider.get_remote_oj()
