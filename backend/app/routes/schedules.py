from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from Functions.Generate_Semester_Schedule_byMajor import generate_full_schedule, convert_schedule_to_obj, add_GER_course, generate_future_schedule, Generate_Schedule_withTime

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
    
    
@router.get("/get_semester_schedule_withGER_by_major_name")
def get_GER_Schedule(major_name: str, startingSem: str = "Fall" , startingYear: int = 0):
    # e.g. input major name: "Bachelor of Arts in Mathematics"
    full_schedule = generate_full_schedule(major_name=major_name, num_semesters=8, min_credits=0, max_credits=18, startingSemester=startingSem)

    # if there is a schedule
    if full_schedule:
        semester_schedules = convert_schedule_to_obj(full_schedule, startYear=startingYear, startsFall= True if startingSem == "Fall" else False)
        GER_schedule = add_GER_course(semester_schedules, isBulePlan=False, isEM=True)
        outputDict = []
        for sem in GER_schedule:
            outputDict.append(sem.to_dict())
        return outputDict
    else:
        return {"Failed to generate a full schedule."} 
    
@router.get("/get_detail_semester_schedule")
def get_Detail_Schedule(major_name: str, startingSem: str = "Fall" , startingYear: int = 0, taken: str = None):

    detial_schedule = Generate_Schedule_withTime(takenClasses= taken, major_name=major_name)[0]
    future_classes = Generate_Schedule_withTime(takenClasses= taken, major_name=major_name)[1]
    if detial_schedule:
        return detial_schedule
    else:
        return {"Failed to generate a schedule."}
    
@router.get("/generate_future_schedule")
def generate_Future_schedule(major_name: str, startingSem: str = "Fall" , startingYear: int = 0, taken: str = None):
    future_schedule = generate_future_schedule(major_name=major_name, num_semesters=7, takenClasses=taken)
    if future_schedule:
        return future_schedule
    else:
        return {"Failed to generate a schedule."}