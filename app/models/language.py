from sqlalchemy import Column, String, Integer
from app.models.base import Base, db


class Language(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    oj = Column(String(100), nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(String(100), nullable=False)

    @staticmethod
    def delete_oj(oj):
        with db.auto_commit():
            Language.query.filter_by(oj=oj).delete()
