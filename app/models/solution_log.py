import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from app.models.base import Base, db
from app.models.solution import Solution


class SolutionLog(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    solution_id = Column(ForeignKey('solution.id'))
    status = Column(String(100), nullable=False)
    create_time = Column(DateTime, nullable=False)

    @classmethod
    def create(cls, **kwargs):
        solution_log = cls()
        with db.auto_commit():
            for key, value in kwargs.items():
                if value is not None:
                    if hasattr(cls, key):
                        setattr(solution_log, key, value)
            if hasattr(cls, 'create_time'):
                setattr(solution_log, 'create_time', datetime.datetime.now())
            db.session.add(solution_log)

            solution = Solution.get_by_id(solution_log.solution_id)
            solution.status = solution_log.status
