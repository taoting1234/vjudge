import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from app.models.base import Base, db
from app.models.solution import Solution


class SolutionLog(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    solution_id = Column(ForeignKey('solution.id'))
    status = Column(String(100), nullable=False)
    captcha = Column(Text)
    create_time = Column(DateTime, nullable=False)

    @staticmethod
    def create_solution_log(solution_id, status, captcha=None):
        with db.auto_commit():
            solution_log = SolutionLog()
            solution_log.solution_id = solution_id
            solution_log.status = status
            solution_log.captcha = captcha
            solution_log.create_time = datetime.datetime.now()
            db.session.add(solution_log)

            solution = Solution.get_by_id(solution_id)
            solution.status = status
