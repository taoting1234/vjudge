from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import AuthFailed
from app.models.base import Base, db


class User(Base):
    username = Column(String(100), primary_key=True)
    _password = Column('password', String(100), nullable=False)
    nickname = Column(String(100))
    permission = Column(Integer, nullable=False, default=0)

    def keys(self):
        return ['username', 'nickname', 'permission']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register(username, password, permission=0):
        with db.auto_commit():
            user = User()
            user.username = username
            user.password = password
            user.permission = permission
            db.session.add(user)

    @property
    def scope(self):
        if self.permission == 1:  # 普通用户
            return 'UserScope'
        elif self.permission == -1:  # 管理员
            return 'AdminScope'
        else:
            return 'UserScope'

    @classmethod
    def verify(cls, username, password):
        user = cls.get_by_id(username)
        if not user.check_password(password):
            raise AuthFailed('username or password wrong')
        return {'uid': user.username}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
