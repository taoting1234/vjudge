from sqlalchemy import Column, String, Integer, Text
from app.models.base import Base, db


class Problem(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    remote_oj = Column(String(100), nullable=False, index=True)
    remote_prob = Column(String(100), nullable=False, index=True)
    title = Column(String(100))
    description = Column(Text)
