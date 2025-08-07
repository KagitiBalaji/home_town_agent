from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CourseRegistration(Base):
    __tablename__ = "course_registrations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    course = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
