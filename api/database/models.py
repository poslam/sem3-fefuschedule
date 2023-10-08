from api.database.database import base
from sqlalchemy import (
    Column,
    Float,
    Integer,
    TIMESTAMP,
    ForeignKey,
    TEXT
)

class Group(base):
    __tablename__ = "group"
    
    id = Column(Integer, primary_key=True)
    
    name = Column(TEXT)
    num = Column(Integer, unique=True)
    

class Class(base):
    __tablename__ = "class"
    
    id = Column(Integer, primary_key=True)
    
    name = Column(TEXT)
    num = Column(Integer, unique=True)
    

# class Event(base):
#     __tablename__ = "project"

#     id = Column(Integer, primary_key=True)
#     name = Column(TEXT)