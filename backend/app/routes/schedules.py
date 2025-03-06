from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from Functions.Generate_Semester_Schedule_byMajor import generate_full_schedule, convert_schedule_to_obj

router = APIRouter()

@router.get("/get_semester_schedule_by_major_name")
def get_Schedule(major_name: str, startingSem: str = "Fall" , startingYear: int = 0):
    # e.g. input major name: "Bachelor of Arts in Mathematics"
    full_schedule = generate_full_schedule(major_name=major_name, num_semesters=8, min_credits=0, max_credits=18, startingSemester=startingSem)

    # if there is a schedule
    if full_schedule:
        semester_schedules = convert_schedule_to_obj(full_schedule, startYear=startingYear, startsFall= True if startingSem == "Fall" else False)
        outputDict = []
        for sem in semester_schedules:
            outputDict.append(sem.to_dict())
        return outputDict
    else:
        return {"Failed to generate a full schedule."}