from fastapi import FastAPI
from routes import users, courses, professors, courses_mongodb, schedules, majorReq
from database import Base, engine
from Functions.Generate_Semester_Schedule_byMajor import generate_full_schedule, convert_schedule_to_obj
from Functions.Get_Class_byID import get_class_by_id
from Functions.Get_Major_Req_byName import get_major_requirements_by_name
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(professors.router, prefix="/professors", tags=["professors"])
app.include_router(courses_mongodb.router, tags=["course_mongodb"])
app.include_router(schedules.router, tags=["schedules"])
app.include_router(majorReq.router, tags=["majorReq"])
