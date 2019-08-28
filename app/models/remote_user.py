import json

from sqlalchemy import Column, String, Integer
from app.models.base import Base


class RemoteUser(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    oj = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100))
    _cookies = Column('cookies', String(10000))
    status = Column(Integer, nullable=False, default=0)

    @property
    def cookies(self):
        try:
            return json.loads(self._cookies)
        except TypeError:
            return None

    @cookies.setter
    def cookies(self, raw):
        self._cookies = json.dumps(raw)
