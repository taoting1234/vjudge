from sqlalchemy import Column, String, Integer, Text
from app.models.base import Base


class Problem(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    remote_oj = Column(String(100), nullable=False)
    remote_prob = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
