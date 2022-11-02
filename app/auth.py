from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from urllib.request import urlopen
import re as r
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from config.settings import SECRET_KEY, ALGORITHM
from app.models import *
from passlib.hash import pbkdf2_sha256
import datetime
import jwt

def token_response(token: str):
    return {
        "access_token": token
    }

async def authenticate_user(email: str, password: str):
    user = await db["user"].find_one({"email": email})
    return pbkdf2_sha256.verify(password, user['password']) if user else False


async def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    payload = {
        "user_id": data['user'],
        "expires": str(datetime.datetime.now() + datetime.timedelta(days=1))
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("user_id")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await db["user"].find_one({"email": payload['user_id']})
    if user is None:
        raise credentials_exception
    return user

