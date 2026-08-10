# models/course.py   (example — replace with your real table/columns)
from sqlalchemy import Column, Integer, String
from db.sqlalchemydb import Base

class CourseModel(Base):
    __tablename__ = "COURSES"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    duration_weeks = Column(Integer)