import datetime

from sqlalchemy import Column, String, Integer, DateTime
from app.models.base import Base
from app.models.contest_problem import ContestProblem


class Contest(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(Integer, nullable=False, index=True)
    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime, index=True)

    @property
    def problem_list(self):
        return ContestProblem.search(contest_id=self.id, page_size=100000)['data']

    @problem_list.setter
    def problem_list(self, raw):
        for problem in self.problem_list:
            problem.delete()

        for problem_id in raw:
            ContestProblem.create(contest_id=self.id, problem_id=problem_id)

    @property
    def status(self):
        now_time = datetime.datetime.now()
        if self.start_time and now_time < self.start_time:
            return 1
        if not self.end_time or now_time < self.end_time:
            return 2
        return 3
