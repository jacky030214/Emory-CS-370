from fastapi import FastAPI
from app.routes import users

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

# Include user routes
app.include_router(users.router, prefix="/users", tags=["users"])
