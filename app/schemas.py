from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email:str
    password:str

class TaskCreate(BaseModel):
    title:str
    description:str
    priority:str

class ProjectCreate(BaseModel):
    name:str
    description:str

class UserResponse(BaseModel):
    id:str
    username:str
    email:str

