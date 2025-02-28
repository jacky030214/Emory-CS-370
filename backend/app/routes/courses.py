from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database

router = APIRouter()

@router.post("/", response_model=schemas.CourseResponse)
def create_course(course: schemas.CourseCreate, db: Session = Depends(database.get_db)):
    professor = crud.get_professor_by_id(db, course.professor_id)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return crud.create_course(db, course)

@router.get("/", response_model=list[schemas.CourseResponse])
def get_all_courses(db: Session = Depends(database.get_db)):
    return crud.get_all_courses(db)

@router.get("/{course_id}", response_model=schemas.CourseResponse)
def get_course_by_id(course_id: int, db: Session = Depends(database.get_db)):
    course = crud.get_course_by_id(db, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/code/{code}", response_model=schemas.CourseResponse)
def get_course_by_code(code: str, db: Session = Depends(database.get_db)):
    course = crud.get_course_by_code(db, code)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course