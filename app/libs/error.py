from flask_restful import abort


class APIException(Exception):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'

    def __init__(self, msg=None):
        if msg:
            self.msg = msg
        abort(self.code, message=self.msg)


class ParameterException(APIException):
    code = 400
    error_code = 1000
    msg = 'invalid parameter'


class AuthFailed(APIException):
    code = 401
    error_code = 1001
    msg = 'authorization failed'


class Forbidden(APIException):
    code = 403
    error_code = 1002
    msg = 'forbidden'


class NotFound(APIException):
    code = 404
    error_code = 1003
    msg = 'the resource are not found O__O...'
