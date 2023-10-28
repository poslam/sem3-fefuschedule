import enum

from sqlalchemy import TEXT, TIMESTAMP, Column, Enum, ForeignKey, Integer

from database.database import base


class FacilitySpec(enum.Enum):
    lecture = "lecture"
    lab_or_prac = "lab_or_prac"


class Group(base):
    __tablename__ = "group"
    
    id = Column(Integer, primary_key=True)
    
    name = Column(TEXT)
    num = Column(Integer, unique=True)

    subgroups_count = Column(Integer)


class User(base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)

    name = Column(TEXT)

    email = Column(TEXT)
    password = Column(TEXT)

    group = Column(ForeignKey(Group.id))
    subgroup = Column(TEXT)
    

class Facility(base):
    __tablename__ = "facility"
    
    id = Column(Integer, primary_key=True)
    
    name = Column(TEXT)
    num = Column(Integer, unique=True)

    spec = Column(Enum(FacilitySpec))


class Teacher(base):
    __tablename__ = "teacher"

    id = Column(TEXT, primary_key=True)

    name = Column(TEXT)


class Event(base):
    __tablename__ = "event"
    
    id = Column(Integer, primary_key=True)

    name = Column(TEXT)
    order = Column(Integer)

    begin = Column(TIMESTAMP)
    end = Column(TIMESTAMP)

    facility = Column(ForeignKey(Facility.id))
    
    capacity = Column(Integer)
    teacher = Column(ForeignKey(Teacher.id))

    group = Column(ForeignKey(Group.id))
    subgroup = Column(TEXT)
    