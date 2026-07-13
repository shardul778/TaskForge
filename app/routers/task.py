from fastapi import APIRouter, Depends, HTTPException
from ..database import get_db 
from ..schemas import TaskCreate
from sqlalchemy.orm import Session 
from ..models import Projects,User,Tasks
from ..auth import verify_token
from sqlalchemy import and_

router = APIRouter()

#create task
@router.post('/projects/{project_id}/tasks')
def create_task(task:TaskCreate,project_id:int, db:Session = Depends(get_db),user = Depends(verify_token)):
    
    current_user = db.query(User).filter(User.username == user).first()
    if not current_user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )
    
    current_project = db.query(Projects).filter(Projects.id==project_id).first()
    if  not current_project:
        raise HTTPException(
            status_code=400,
            detail="Project does not exists"
        )
    
    verify_user = db.query(Projects).filter(and_(Projects.owner_id==current_user.id,Projects.id==project_id)).first()
    if not verify_user:
            raise HTTPException(
            status_code=400,
            detail="Project is not yours"
        )

    task_created = Tasks(title= task.title , description = task.description,priority=task.priority,owner_id=current_user.id,project_id=current_project.id)
    current_task = db.query(Tasks).filter(and_(Tasks.title == task.title,Tasks.project_id==current_project.id)).first()
    if current_task:
        raise HTTPException(
            status_code=400,
            detail="Task already exists"
        )

    db.add(task_created)
    db.commit()
    db.refresh(task_created)

    return{
        "project":"Task created",
        'name':task_created.title,
         'description':task_created.description   
         }


#get all the task
@router.get('/projects/{project_id}/tasks')
def get_tasks(project_id:int,db:Session = Depends(get_db),user = Depends(verify_token)):
    
    current_user = db.query(User).filter(User.username == user).first()
    if not current_user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )
    
    current_project = db.query(Projects).filter(Projects.id==project_id).first()
    if  not current_project:
        raise HTTPException(
            status_code=400,
            detail="Project does not exists"
        )
    
    verify_user = db.query(Projects).filter(and_(Projects.owner_id==current_user.id,Projects.id==project_id)).first()
    if not verify_user:
            raise HTTPException(
            status_code=400,
            detail="Project is not yours"
        )
    
    get_tasks = db.query(Tasks).filter(and_(Tasks.owner_id==current_user.id,Tasks.project_id==project_id)).all()

    return{
        "project":get_tasks 
         }

#get specific task
@router.get('/projects/{project_id}/tasks/{task_id}')
def get_task(task_id:int,project_id:int, db:Session = Depends(get_db),user = Depends(verify_token)):
    
    current_user = db.query(User).filter(User.username == user).first()
    if not current_user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )
    get_task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if  get_task:
        verify_user = db.query(Tasks).filter(and_(Tasks.project_id==project_id,Tasks.owner_id==current_user.id)).first()
        if not verify_user:
            raise HTTPException(
            status_code=400,
            detail="Task is not yours"
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Task not found"
        )

    return{
        "project":get_task 
         }


#update the project
@router.put('/projects/{project_id}/tasks/{task_id}')
def update_task(project_id:int,task_id:int ,title:str,priority:str, description:str ,  db:Session = Depends(get_db),user = Depends(verify_token)):
    
    current_user = db.query(User).filter(User.username == user).first()
    if not current_user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    current_task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if  current_task:
        verify_user = db.query(Tasks).filter(and_(Tasks.project_id==project_id,Tasks.owner_id==current_user.id)).first()
        if not verify_user:
            raise HTTPException(
            status_code=400,
            detail="Task is not yours"
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Task not found"
        )
    
    current_task.description = description
    current_task .title = title
    current_task.priority = priority
    current_task.completed = False

    
    db.commit()
    db.refresh(current_task)

    return{
        "project":"Task update",
         "data":current_task   
         }


#delete the project
@router.delete('/projects/{project_id}/tasks/{task_id}')
def delete_task(project_id:int,task_id:int ,  db:Session = Depends(get_db),user = Depends(verify_token)):
    
    current_user = db.query(User).filter(User.username == user).first()
    if not current_user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    current_task= db.query(Tasks).filter(Tasks.id == task_id).first()
    if  current_task:
        verify_user = db.query(Tasks).filter(and_(Tasks.project_id==project_id,Tasks.owner_id==current_user.id)).first()
        if not verify_user:
            raise HTTPException(
            status_code=400,
            detail="Task is not yours"
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Task not found"
        )
    
    db.delete(current_task)    
    db.commit()

    return{
        "project":"Task deleted",
          
         }

