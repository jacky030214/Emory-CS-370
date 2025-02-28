from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, nullable=False) # no need for unique=True because this is primary key
    name = Column(String, nullable=False)
    code = Column(String, index=True, nullable=False, unique=True) # index=True will help fasten query responses
    description = Column(String)
    recurring = Column(Boolean, default=False)
    credit_hours = Column(Integer, nullable=False)
   
    # TODO: Update the properties of these; enforce limited options of reqs and campus?; how to make preqs a list of Course objs?
    prerequisites = Column(String)
    requirement_designation = Column(String)
    campus = Column(String)
    # TODO: add department? already in Professor

    professor_id = Column(Integer, ForeignKey("professors.id"))
    professor = relationship("Professor", back_populates="courses") # define a bidirectional relationship between courses and professors


class Professor(Base):
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    department = Column(String)

    courses = relationship("Course", back_populates="professor")
