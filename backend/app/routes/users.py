from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database
from Functions.Create_User import generate_User, login
from Functions.Generate_Semester_Schedule_byMajor import generate_full_schedule, convert_schedule_to_obj, add_GER_course, generate_future_schedule, Generate_Schedule_withTime
from Models.User_Logins_Model import User_Logins
from routes.schedules import get_GER_Schedule
from pymongo import MongoClient

router = APIRouter()
"""

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.create_user(db, user)
    return db_user

@router.get("/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(database.get_db)):
    return crud.get_all_users(db)

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/username/{username}", response_model=schemas.UserResponse)
def get_user_by_username(username: str, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/email/{email}", response_model=schemas.UserResponse)
def get_user_by_email(email: str, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/login", response_model=schemas.UserResponse)
def login(email: str, input_pass: str, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not crud.verify_password(input_pass, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    return db_user
"""

@router.post("/create user")
def create_user(email: str, password: str, username: str):
    return generate_User(email, password, username)

@router.get("/Login")
def User_login(account: str, password: str):
    return login(account, password)

@router.post("/create schedule")
def create_schedule(account: str, major_name: str, startingSem: str = "Fall" , startingYear: int = 0):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["my_database"]
    
    # Access the collection that stores major requirements
    collection = db["Users"]
    
    full_schedule = generate_full_schedule(major_name=major_name, num_semesters=8, min_credits=0, max_credits=18, startingSemester=startingSem)

    # if there is a schedule
    if full_schedule:
        semester_schedules = convert_schedule_to_obj(full_schedule, startYear=startingYear, startsFall= True if startingSem == "Fall" else False)
        GER_schedule = add_GER_course(semester_schedules, isBulePlan=False, isEM=True)
        outputDict = []

        for sem in GER_schedule:
            outputDict.append(sem.to_dict())
        user = collection.find_one({"email": account})
        if not user:
            user = collection.find_one({"username": account})
            if not user:
                return "User not exist"

            collection.update_one({"username": account}, {"$set": {"schedule": outputDict}})
            return {"message": "Schedule updated"}
            
        collection.update_one({"email": account}, {"$set": {"schedule": outputDict}})
        return {"message": "Schedule updated"}
    else:
        return {"Failed to generate a full schedule."}
    
@router.get("/get current schedule")
def get_user_schedule(account: str):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["my_database"]
    
    # Access the collection that stores major requirements
    collection = db["Users"]
    
    user = collection.find_one({"email": account})
    if not user:
        user = collection.find_one({"username": account})
        if not user:
            return "User not exist"
        if "schedule" not in user:
            return {"no schedule found for": user['username']}
        schedule = user['schedule']
    if "schedule" not in user:
        return {"no schedule found for": user['username']}
    schedule = user['schedule']
    
    if schedule:
        return {"current schedule for": user['username'], "\n": schedule}
    else: 
        return {"no schedule found for": user['username']}
    
@router.post("/generate detial schedule")
def generate_detail_schedule(account: str, major_name: str, startingSem: str = "Fall" , startingYear: int = 0, taken: list[str] = None):

    client = MongoClient("mongodb://localhost:27017/")
    db = client["my_database"]
    
    # Access the collection that stores major requirements
    collection = db["Users"]
    
    user = collection.find_one({"email": account})
    if not user:
        user = collection.find_one({"username": account})
        if not user:
            return "User not exist"
    if user['takenClasses']:
        takenClasses = user['takenClasses']
        for cls in takenClasses:
            taken.append(cls)
    id = user['_id']

    detail_schedule = Generate_Schedule_withTime(takenClasses= taken, major_name=major_name)[0]
    future_classes = Generate_Schedule_withTime(takenClasses= taken, major_name=major_name)[1]   
    if detail_schedule:
        # if not user:
        #     user = collection.find_one({"username": account})
        #     if not user:
        #         return "User not exist"

        #     collection.update_one({"username": account}, {"$set": {
        #         "detail_Schedule": detail_schedule,
        #         "futureClasses": future_classes,
        #         "majorName": major_name
        #     }})
        #     return {"message": "Schedule updated"}
            
        # return {"message": "Schedule updated"}.

        detail_schedule = detail_schedule.to_dict()
        collection.update_one({"_id": id}, {"$set": {
            "detail_Schedule": detail_schedule,
            "futureClasses": future_classes,
            "majorName": major_name,
            "takenClasses": taken
        }})  
        return {"message": "Schedule updated"}
    else:
        return {"Failed to generate a schedule."}
    
