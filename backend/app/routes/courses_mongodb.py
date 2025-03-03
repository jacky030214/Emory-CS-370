from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from Functions.Get_Class_byID import get_class_by_id

router = APIRouter()


@router.get("/get class by class id")
def get_Class(class_id: str):
    class_obj = get_class_by_id(class_id)
    if class_obj:
        return class_obj.to_dict()
    else:
        return {"Failed to find such class: " + class_id}