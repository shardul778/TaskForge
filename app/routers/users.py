from fastapi import APIRouter, Depends, HTTPException
from ..schemas import UserCreate
from ..database import get_db
from sqlalchemy.orm import Session
from ..auth import hash_password , verify_password,create_token,verify_token
from ..models import User
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_

router = APIRouter()

@router.post('/register')
def register_user(user:UserCreate,db:Session = Depends(get_db)):
    hpassword = hash_password(user.password)
    
    existing_user = db.query(User).filter(or_(User.email == user.email,User.username == user.username)).first()
    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(
            status_code=400,
            detail = "Username already exist"
        )
        if existing_user.email == user.email:
            raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    user_created = User(username=user.username , email=user.email , password = hpassword)
    db.add(user_created)
    db.commit()
    db.refresh(user_created)
    return {
    "message":"User created",
    "username":user_created.username,
    "email":user_created.email
}
    
@router.post("/login")
def login_user( form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail = "User does not exist"
        )
    if not verify_password(form_data.password,user.password):
        raise HTTPException(
            status_code=401,
            detail = "Invalid username or password"
        )

    token = create_token({
        "sub":user.username
    })
    
    return{
        "access_token":token,
        "token_type":"bearer"
    }

@router.get("/me")
def me_user( username:str = Depends(verify_token)):   
    return {
        "message":"hello user",
        "user":username
    }
    


    


