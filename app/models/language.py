from sqlalchemy import Column, String, Integer
from app.models.base import Base, db


class Language(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    oj = Column(String(100), nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(String(100), nullable=False)

    @staticmethod
    def create_language(oj, key, value):
        with db.auto_commit():
            language = Language()
            language.oj = oj
            language.key = key
            language.value = value
            db.session.add(language)

    @staticmethod
    def delete_all():
        with db.auto_commit():
            Language.query.delete()
