from fastapi import APIRouter, Depends, HTTPException
from ..database import get_db 
from ..schemas import ProjectCreate
from sqlalchemy.orm import Session 
from ..models import Projects,User
from ..auth import verify_token,oauth2_schema
from sqlalchemy import and_
from ..redis import r
import json

router = APIRouter()

#create project
@router.post('/projects')
def create_project(project:ProjectCreate, db:Session = Depends(get_db),user = Depends(verify_token)):
    
    current_user = db.query(User).filter(User.username == user).first()
    if not current_user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )
    project_created = Projects(name= project.name , description = project.description,owner_id=current_user.id)
    current_project = db.query(Projects).filter(and_(Projects.name == project.name,Projects.owner_id==current_user.id)).first()
    if current_project:
        raise HTTPException(
            status_code=409,
            detail="Project already exists"
        )
    cache_key = f"projects_{current_user.id}"

    db.add(project_created)
    db.commit()
    db.refresh(project_created)
    r.delete(cache_key)

    return{
        "project":"Project saved",
        'name':project_created.name,
         'description': project_created.description   
         }


#get all the project
@router.get('/projects')
def get_projects(db:Session = Depends(get_db),user = Depends(verify_token)):
    
    current_user = db.query(User).filter(User.username == user).first()
    if not current_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    cache_key = f"projects_{current_user.id}"
    info = r.get(cache_key)
    if info is not None:
        project_data = json.loads(info)
    else:
        get_projects = db.query(Projects).filter(Projects.owner_id==current_user.id).all()
        project_data = [
    {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "owner_id": project.owner_id
    }
    for project in get_projects
]

        data = json.dumps(project_data)
        r.setex(cache_key,300,data)

    return{
        "project":project_data 
         }

#get specific project
@router.get('/projects/{project_id}')
def get_project(project_id:int, db:Session = Depends(get_db),user = Depends(verify_token)):
    
    current_user = db.query(User).filter(User.username == user).first()
    if not current_user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    cache_key = f"projects_{current_user.id}"
    info = r.get(cache_key)
    if info is not None:
        project_data = json.loads(info)
    else:
        get_projects = db.query(Projects).filter(Projects.id == project_id).first()
        project_data = [
    {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "owner_id": project.owner_id
    }
    for project in get_projects
]

        data = json.dumps(project_data)
        r.setex(cache_key,300,data)

    if  project_data:
        verify_user = db.query(Projects).filter(and_(Projects.owner_id==current_user.id,Projects.id==project_id)).first()
        if not verify_user:
            raise HTTPException(
            status_code=400,
            detail="Project is not yours"
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Project not found"
        )

    return{
        "project":project_data
         }


#update the project
@router.put('/projects/{project_id}')
def update_project(project_id:int , description:str ,  db:Session = Depends(get_db),user = Depends(verify_token)):
    
    current_user = db.query(User).filter(User.username == user).first()
    if not current_user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    current_project = db.query(Projects).filter(Projects.id == project_id).first()
    if  current_project:
        verify_user = db.query(Projects).filter(and_(Projects.owner_id==current_user.id,Projects.id==project_id)).first()
        if not verify_user:
            raise HTTPException(
            status_code=400,
            detail="Project is not yours"
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Project not found"
        )
    
    current_project.description = description
    cache_key = f"projects_{current_user.id}"

    
    db.commit()
    db.refresh(current_project)
    r.delete(cache_key)

    return{
        "project":"Project update",
         "data":current_project   
         }


#delete the project
@router.delete('/projects/{project_id}')
def delete_project(project_id:int ,  db:Session = Depends(get_db),user = Depends(verify_token)):
        
    current_user = db.query(User).filter(User.username == user).first()
    if not current_user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    current_project = db.query(Projects).filter(Projects.id == project_id).first()
    if  current_project:
        verify_user = db.query(Projects).filter(and_(Projects.owner_id==current_user.id,Projects.id==project_id)).first()
        if not verify_user:
            raise HTTPException(
            status_code=400,
            detail="Project is not yours"
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Project not found"
        )
    cache_key = f"projects_{current_user.id}"
    
    db.delete(current_project)    
    db.commit()
    r.delete(cache_key)

    return{
        "project":"Project deleted",
          
         }

