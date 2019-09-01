import hashlib
import time
from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired
from app.config.secure import WHITELIST_UA, SECRET_KEY
from app.libs.error import NotFound, Forbidden, AuthFailed
from app.libs.scope import is_in_scope
from app.models.user import User

auth = HTTPBasicAuth()


def md5(raw):
    return hashlib.md5(raw.encode('utf8')).hexdigest()


@auth.verify_password
def verify_token(token, secret):
    ua = request.headers.get('User-Agent', '')
    if ua != WHITELIST_UA:
        timestamp = int(request.headers.get('Timestamp', 0))
        if abs(timestamp - int(time.time())) > 10:
            raise AuthFailed()

        my_secret = md5(token + str(timestamp))
        if my_secret != secret:
            raise AuthFailed()

    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed('token is invalid')
    except SignatureExpired:
        raise AuthFailed('token is expired')
    uid = data['uid']
    user = User.get_by_id(uid)
    if not user:
        raise NotFound()
    allow = is_in_scope(user.scope, request.endpoint)
    if not allow:
        raise Forbidden()
    g.user = user
    return True

def generate_auth_token(uid, expiration):
    """生成令牌"""
    s = Serializer(SECRET_KEY, expires_in=expiration)
    return s.dumps({'uid': uid}).decode('ascii')