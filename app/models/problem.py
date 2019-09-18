from sqlalchemy import Column, String, Integer, Text
from app.models.base import Base, db
from app.models.solution import Solution


class Problem(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    remote_oj = Column(String(100), nullable=False, index=True)
    remote_prob = Column(String(100), nullable=False, index=True)
    title = Column(String(100))
    description = Column(Text)
    status = Column(Integer, nullable=False, index=True)

    @property
    def accept_number(self):
        return Solution.query.filter_by(problem_id=self.id, status_canonical='AC').count()

    @property
    def submit_number(self):
        return Solution.query.filter_by(problem_id=self.id).count()
