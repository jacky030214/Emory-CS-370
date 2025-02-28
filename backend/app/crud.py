# CRUD stands for Create, Read, Update, and Delete. These are the four basic operations for managing data in a database

from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext

"""
    User CRUD operations
"""

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(input_pass: str, true_pass: str) -> bool:
    return pwd_context.verify(input_pass, true_pass) # true_pass is hashed

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_all_users(db: Session):
    return db.query(models.User).all()

"""
    Course CRUD operations
"""

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_all_courses(db: Session):
    return db.query(models.Course).all()

def get_course_by_id(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

def get_course_by_code(db: Session, code: str):
    return db.query(models.Course).filter(models.Course.code == code).first()

"""
    Professor CRUD operations
"""

def create_professor(db: Session, professor: schemas.ProfessorCreate):
    db_professor = models.Professor(**professor.model_dump())
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

def get_all_professors(db: Session):
    return db.query(models.Professor).all()

def get_professor_by_id(db: Session, professor_id: int):
    return db.query(models.Professor).filter(models.Professor.id == professor_id).first()

def get_professor_by_name(db: Session, first_name: str, last_name: str):
    return db.query(models.Professor).filter(models.Professor.first_name == first_name, models.Professor.last_name == last_name).first()