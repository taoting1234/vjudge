from flask_restful import abort
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.base import Base


class User(Base):
    id = Column(String(100), primary_key=True)
    _password = Column('password', String(100), nullable=False)
    nickname = Column(String(100))
    permission = Column(Integer, nullable=False, default=0)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @property
    def scope(self):
        if self.permission == 1:  # 普通用户
            return 'UserScope'
        elif self.permission == -1:  # 管理员
            return 'AdminScope'
        else:
            return 'UserScope'

    @classmethod
    def verify(cls, id_, password):
        user = cls.get_by_id(id_)
        if not user.check_password(password):
            abort(401, message='id or password wrong')
        return {'uid': user.id}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
