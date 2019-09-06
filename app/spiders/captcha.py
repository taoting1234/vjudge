import random

import requests

from app.config.secure import lianzhong_software_id, lianzhong_software_secret, lianzhong_username, \
    lianzhong_password
from app.spiders.helper import get_base64


class Lianzhong:
    software_id = lianzhong_software_id
    software_secret = lianzhong_software_secret
    username = lianzhong_username
    password = lianzhong_password

    @classmethod
    def recognize(cls, img, type_='1008', min_=7, max_=7):
        img = get_base64(img)
        url = 'https://v2-api.jsdama.com/upload'
        data = {
            'softwareId': cls.software_id,
            'softwareSecret': cls.software_secret,
            'username': cls.username,
            'password': cls.password,
            'captchaData': img,
            'captchaType': type_,
            'captchaMinLength': min_,
            'captchaMaxLength': max_
        }
        res = requests.post(url, json=data).json()
        if res.get('code'):
            return {
                'success': False,
                'message': res.get('message')
            }
        return {
            'success': True,
            'captcha_id': res['data']['captchaId'],
            'result': res['data']['recognition']
        }

    @classmethod
    def report(cls, captcha_id):
        url = 'https://v2-api.jsdama.com/report-error'
        data = {
            'softwareId': cls.software_id,
            'softwareSecret': cls.software_secret,
            'username': cls.username,
            'password': cls.password,
            'captchaId': captcha_id,
        }
        requests.post(url, json=data)


def save_captcha(img, result):
    with open('captcha/{}_{}.jpg'.format(result, random.randint(100000, 999999)), 'wb') as f:
        f.write(img)
