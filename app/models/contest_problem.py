from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from app.models.base import Base


class ContestProblem(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    contest_id = Column(ForeignKey('contest.id'))
    problem_id = Column(ForeignKey('problem.id'))
