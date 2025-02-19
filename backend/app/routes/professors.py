from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database

router = APIRouter()

@router.post("/", response_model=schemas.ProfessorResponse)
def create_professor(professor: schemas.ProfessorCreate, db: Session = Depends(database.get_db)):
    return crud.create_professor(db, professor)

@router.get("/", response_model=list[schemas.ProfessorResponse])
def get_all_professors(db: Session = Depends(database.get_db)):
    return crud.get_all_professors(db)

@router.get("/{professor_id}", response_model=schemas.ProfessorResponse)
def get_professor_by_id(professor_id: int, db: Session = Depends(database.get_db)):
    professor = crud.get_professor_by_id(db, professor_id)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor

@router.get("/name/{name}", response_model=schemas.ProfessorResponse)
def get_professor_by_name(name: str, db: Session = Depends(database.get_db)):
    first_name, last_name = name.split()[0], name.split()[-1]
    professor = crud.get_professor_by_name(db, first_name, last_name)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor