from fastapi import APIRouter, Depends, HTTPException
from ..database import get_db 
from ..schemas import TaskCreate
from sqlalchemy.orm import Session 
from ..models import Projects,User,Tasks
from ..auth import verify_token
from sqlalchemy import and_
from ..redis import r
import json

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
    cache_key = f"tasks_{current_user.id}_{project_id}"

    db.add(task_created)
    db.commit()
    db.refresh(task_created)
    r.delete(cache_key)

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
    
    cache_key = f"tasks_{current_user.id}_{project_id}"
    info = r.get(cache_key)
    if info is not None:
        task_data = json.loads(info)
    else:
        get_tasks = db.query(Tasks).filter(and_(Tasks.owner_id==current_user.id,Tasks.project_id==project_id)).all()
        task_data = [
    {
        "id": task.id,
        "title" : task.title,
        "completed": task.completed,
        "description": task.description,
        "projectid": task.project_id,
        "priority":task.priority,
        "owner_id": task.owner_id
    }
    for task in get_tasks
]

        data = json.dumps(task_data)
        r.setex(cache_key,300,data)

    return{
        "task":task_data 
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
    
    if not get_task:
        raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
    
    cache_key = f"task_{current_user.id}_{project_id}_{task_id}"
    info = r.get(cache_key)
    if info is not None:
        task_data = json.loads(info)
    else:
        get_tasks = db.query(Tasks).filter(
    and_(
        Tasks.id == task_id,
        Tasks.project_id == project_id,
        Tasks.owner_id == current_user.id
    )
).first()
        task_data = {
    
        "id": get_tasks.id,
        "title" : get_tasks.title,
        "completed": get_tasks.completed,
        "description": get_tasks.description,
        "projectid": get_tasks.project_id,
        "priority":get_tasks.priority,
        "owner_id": get_tasks.owner_id
    }
    


        data = json.dumps(task_data)
        r.setex(cache_key,300,data)


    if  task_data:
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
        "task":task_data 
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

    cache_key = f"task_{current_user.id}_{project_id}_{task_id}"
    
    db.commit()
    db.refresh(current_task)
    r.delete(cache_key)

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
    
    cache_key = f"task_{current_user.id}_{project_id}_{task_id}"

    db.delete(current_task)    
    db.commit()
    r.delete(cache_key)

    return{
        "project":"Task deleted",
          
         }

