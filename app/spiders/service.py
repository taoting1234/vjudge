import base64


def encode_base64(raw):
    return base64.b64encode(raw.encode('utf8')).decode()


if __name__ == '__main__':
    print(encode_base64('11111111111111111111'))
