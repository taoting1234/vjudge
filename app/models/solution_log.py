from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from app.models.base import Base


class SolutionLog(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    solution_id = Column(ForeignKey('solution.id'), index=True)
    status = Column(String(100), nullable=False)
    create_time = Column(DateTime, nullable=False, index=True)
