from app.database import Base, engine
from sqlalchemy import Column,Integer,String,Boolean

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String)
    email=Column(String)
    password=Column(String)

class Tasks(Base):
    __tablename__="tasks"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    description=Column(String)
    completed=Column(Boolean,default = False)
    priority=Column(String)
    project_id=Column(Integer)
    owner_id=Column(Integer)

class Projects(Base):
    __tablename__="projects"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    description=Column(String)
    owner_id=Column(Integer)

Base.metadata.create_all(bind=engine)