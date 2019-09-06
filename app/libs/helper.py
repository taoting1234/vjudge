import base64
import hashlib


def get_base64(raw):
    if isinstance(raw, str):
        raw = raw.encode('utf8')
    return base64.b64encode(raw).decode()


def get_md5(raw):
    if isinstance(raw, str):
        raw = raw.encode('utf8')
    return hashlib.md5(raw).hexdigest()


if __name__ == '__main__':
    print(get_md5('990718'))
