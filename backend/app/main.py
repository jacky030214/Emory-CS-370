from fastapi import FastAPI
from app.routes import users, courses, professors
from app.database import Base, engine

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(professors.router, prefix="/professors", tags=["professors"])
