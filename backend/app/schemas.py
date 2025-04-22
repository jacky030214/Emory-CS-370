from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    # Config class of a Pydantic model allows the model to work seamlessly with 
    # ORMs (Object-Relational Mappers) like SQLAlchemy. When orm_mode is set to 
    # True, Pydantic models can be populated not just from dictionaries but also
    # from ORM objects. This is useful when you are working with databases and
    # want to convert database records into Pydantic models for validation or 
    # serialization.
    class Config:
        orm_mode = True
        
class CourseCreate(BaseModel):
    name: str
    code: str
    description: str
    recurring: bool
    credit_hours: int
    prerequisites: str
    requirement_designation: str
    campus: str
    professor_id: int

class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    description: str
    recurring: bool
    credit_hours: int
    prerequisites: str
    requirement_designation: str
    campus: str
    professor_id: int
    professor: ProfessorResponse | None = None

    class Config:
        orm_mode = True

class ProfessorCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department: str

class ProfessorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department: str

    class Config:
        orm_mode = True