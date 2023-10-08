from database.database import base
from sqlalchemy import (
    Column,
    Integer,
    TEXT
)

class Group(base):
    __tablename__ = "group"
    
    id = Column(Integer, primary_key=True)
    
    name = Column(TEXT)
    num = Column(Integer, unique=True)
    

class Facility(base):
    __tablename__ = "facility"
    
    id = Column(Integer, primary_key=True)
    
    name = Column(TEXT)
    num = Column(Integer, unique=True)


class Teacher(base):
    __tablename__ = "teacher"

    id = Column(TEXT, primary_key=True)

    name = Column(TEXT)
