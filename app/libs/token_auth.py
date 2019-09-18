import functools
import time
from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired
from app.config.secure import WHITELIST_UA, SECRET_KEY
from app.libs.error import Forbidden, AuthFailed
from app.models.user import User
from app.libs.helper import get_md5

auth = HTTPBasicAuth()


@auth.verify_password
def verify_token(token, secret):
    g.user = get_current_user()
    if not g.user:
        raise AuthFailed()
    return True


def get_current_user():
    token = auth.get_auth()['username']
    secret = auth.get_auth()['password']
    ua = request.headers.get('User-Agent', '')
    if ua != WHITELIST_UA:
        timestamp = int(request.headers.get('Timestamp', 0))
        if abs(timestamp - int(time.time())) > 60:
            return None

        my_secret = get_md5(token + str(timestamp))
        if my_secret != secret:
            return None

    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        return None
    except SignatureExpired:
        return None
    uid = data['uid']
    return User.get_by_id(uid)


def generate_auth_token(uid, expiration):
    s = Serializer(SECRET_KEY, expires_in=expiration)
    return s.dumps({'uid': uid}).decode('ascii')


def self_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get('id_'):
            if g.user.id != kwargs['id_'] and g.user.permission != -1:
                raise Forbidden()
        return func(*args, **kwargs)

    return wrapper


def admin_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if g.user.permission != -1:
            raise Forbidden()
        return func(*args, **kwargs)

    return wrapper
