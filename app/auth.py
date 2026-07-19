from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from redis import r

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

# password hashing setup
pwd_context = CryptContext(schemes = ["bcrypt"] , deprecated = 'auto')

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

#hash password
def hash_password(password:str):
    return pwd_context.hash(password)

#verify password
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

#creating  token
def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp":expire
    })
    token =jwt.encode(to_encode,SECRET_KEY,algorithm = ALGORITHM)

    return token

#verify token and use redis
def verify_token(token:str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms = [ALGORITHM])
        username :str = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=401,
                detail = "Invalid token"
            )
        
        check_user =  r.get(token)
        if check_user == "blacklisted":
            raise HTTPException(
            status_code=401,
            detail="Token has been blacklisted"
        )
        return username
    except JWTError:
        raise HTTPException(
                status_code=401,
                detail = "Invalid token"
        )
    

    


