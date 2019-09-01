from contextlib import contextmanager
from flask_sqlalchemy import BaseQuery
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import desc


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


db = SQLAlchemy(query_class=BaseQuery)


class Base(db.Model):
    __abstract__ = True
    __table_args__ = {"useexisting": True}

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def create(cls, **kwargs):
        base = cls()
        with db.auto_commit():
            for key, value in kwargs.items():
                if value is not None:
                    if hasattr(cls, key):
                        setattr(base, key, value)
            db.session.add(base)

    def modify(self, **kwargs):
        with db.auto_commit():
            for key, value in kwargs.items():
                if value is not None:
                    if hasattr(self, key):
                        setattr(self, key, value)

    @classmethod
    def search(cls, **kwargs):
        res = cls.query
        for key, value in kwargs.items():
            if value is not None:
                try:
                    value = int(value)
                except ValueError:
                    pass
                if hasattr(cls, key):
                    if isinstance(value, int):
                        res = res.filter(getattr(cls, key) == value)
                    else:
                        res = res.filter(getattr(cls, key).like(value))

        if hasattr(cls, 'id'):
            res = res.order_by(desc(cls.id))
        page = int(kwargs.get('page')) if kwargs.get('page') else 1
        page_size = int(kwargs.get('page_size')) if kwargs.get('page_size') else 20
        data = {
            'meta': {
                'count': res.count(),
                'page': page,
                'page_size': page_size
            }
        }
        res = res.offset((page - 1) * page_size).limit(page_size)
        res = res.all()
        data['data'] = res
        return data
