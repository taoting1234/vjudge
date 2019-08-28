import datetime

from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from app.models.base import Base, db
from app.models.solution_log import SolutionLog


class Solution(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    problem_id = Column(ForeignKey('problem.id'))
    username = Column(ForeignKey('user.username'))
    code = Column(Text, nullable=False)
    language = Column(String(100), nullable=False)
    language_canonical = Column(String(100), nullable=False)
    status = Column(String(100), nullable=False)
    status_canonical = Column(String(100), nullable=False)
    processing = Column(Integer, nullable=False)
    length = Column(Integer, nullable=True)
    remote_run_id = Column(String(100))
    additional_info = Column(Text)
    create_time = Column(DateTime, nullable=False)

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
        else:
            return "OTHER"

    def get_language_canonical(self):
        if "c++" in self.language.lower():
            return "C++"
        elif "c#" in self.language.lower():
            return "C#"
        elif "pascal" in self.language.lower():
            return "PASCAL"
        elif "java" in self.language.lower():
            return "JAVA"
        elif "python" in self.language.lower():
            return "PYTHON"
        elif "ruby" in self.language.lower():
            return "RUBY"
        elif "c" in self.language.lower():
            return "C"
        else:
            return "OTHER"

    def get_length(self):
        return len(self.code)

    def update_status(self):
        self.language_canonical = self.get_language_canonical()
        self.status_canonical = self.get_status_canonical()
        self.length = self.get_length()

    @staticmethod
    def create_solution(problem_id, username, code, language, status='create solution'):
        with db.auto_commit():
            solution = Solution()
            solution.problem_id = problem_id
            solution.username = username
            solution.code = code
            solution.language = language
            solution.status = status
            solution.create_time = datetime.datetime.now()
            solution.processing = 1
            solution.update_status()
            db.session.add(solution)

        SolutionLog.create_solution_log(solution.id, status)

    def modify(self, **kwargs):
        with db.auto_commit():
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            self.update_status()
