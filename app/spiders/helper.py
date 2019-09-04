import base64
import hashlib


def get_base64(raw):
    return base64.b64encode(raw.encode('utf8')).decode(),


def get_md5(raw):
    return hashlib.md5(raw.encode('utf8')).hexdigest()


if __name__ == '__main__':
    print(get_md5('990718'))
