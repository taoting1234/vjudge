import datetime
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from app.models.base import Base, db
# 导入
from app.models.remote_user import RemoteUser
from app.models.contest import Contest
from app.models.solution_log import SolutionLog


class Solution(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    problem_id = Column(ForeignKey('problem.id'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    code = Column(Text, nullable=False)
    language = Column(String(100), nullable=False)
    language_canonical = Column(String(100), nullable=False, index=True)
    status = Column(String(100), nullable=False)
    status_canonical = Column(String(100), nullable=False, index=True)
    run_time = Column(Integer, index=True)
    run_memory = Column(Integer, index=True)
    processing = Column(Integer, nullable=False, index=True)
    length = Column(Integer, nullable=True, index=True)
    remote_id = Column(String(100))
    remote_user_id = Column(ForeignKey('remote_user.id'), index=True)
    additional_info = Column(Text)
    contest_id = Column(ForeignKey('contest.id'), index=True)
    create_time = Column(DateTime, nullable=False, index=True)

    @property
    def solution_log(self):
        return SolutionLog.search(solution_id=self.id, page_size=100000)['data']

    def get_status_canonical(self):
        if "accepted" in self.status.lower():
            return "AC"
        elif "wrong answer" in self.status.lower():
            return "WA"
        elif "compilation error" in self.status.lower() or "compile error" in self.status.lower():
            return "CE"
        elif "presentation error" in self.status.lower():
            return "PE"
        elif "time limit exceed" in self.status.lower():
            return "TLE"
        elif "memory limit exceed" in self.status.lower():
            return "MLE"
        elif "output limit exceed" in self.status.lower():
            return "OLE"
        elif "runtime error" in self.status.lower():
            return "RE"
        elif self.processing == 1:
            return "PENDING"
        else:
            return "SE"

    def get_language_canonical(self):
        if "c++" in self.language.lower() or "g++" in self.language.lower():
            return "C++"
        elif "c#" in self.language.lower():
            return "C#"
        elif "pascal" in self.language.lower():
            return "PASCAL"
        elif "java" in self.language.lower():
            return "JAVA"
        elif "py" in self.language.lower():
            return "PYTHON"
        elif "ruby" in self.language.lower():
            return "RUBY"
        elif "c" in self.language.lower() or "gcc" in self.language.lower():
            return "C"
        else:
            return "OTHER"

    def get_code_length(self):
        return len(self.code)

    def update_status(self):
        self.language_canonical = self.get_language_canonical()
        self.status_canonical = self.get_status_canonical()

    @classmethod
    def create(cls, **kwargs):
        solution = cls()
        with db.auto_commit():
            for key, value in kwargs.items():
                if value is not None:
                    if hasattr(cls, key):
                        setattr(solution, key, value)
            if hasattr(cls, 'create_time'):
                setattr(solution, 'create_time', datetime.datetime.now())
            solution.length = solution.get_code_length()
            solution.processing = 1
            solution.update_status()
            db.session.add(solution)

        SolutionLog.create(solution_id=solution.id, status=kwargs['status'])
        return solution

    def modify(self, **kwargs):
        with db.auto_commit():
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            self.update_status()

        SolutionLog.create(solution_id=self.id, status=kwargs['status'])
