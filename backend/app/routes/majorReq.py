from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from Functions.Get_Major_Req_byName import get_major_requirements_by_name

router = APIRouter()

@router.get("/get major requirement by major name")
def get_MajorReq(major_name: str):
    majorReq = get_major_requirements_by_name(major_name)
    if majorReq:
        return majorReq.to_dict()
    else:
        return {"Failed to get such major: " + major_name}