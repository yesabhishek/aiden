from PIL import Image
import pytesseract
from fastapi import FastAPI,  status, File, BackgroundTasks, Request , Header, Form
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os
import io
from fastapi.staticfiles import StaticFiles
import re 
import socket
from urllib.request import urlopen
import re as r
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.auth import *
from app.models import *
from config.settings import *
from fastapi.encoders import jsonable_encoder
import json

# Creating a FastAPI app.
app = FastAPI(
    title="Aiden API",
    version="0.1",
    contact={
        'name': "Abhishek Choudhury",
        'url': 'https://abhishekchoudhury.in',
    })


# Mounting the static folder in the root directory of the project.
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.post("/sign_up", response_model=User)
async def sign_up(username:str = Form(), email:str = Form(), password:str = Form(),):
    user = {
        'username': username,
        'email': email,
        'password': password,
    }
    new_user = await db["user"].insert_one(user)
    created_user = await db["user"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=str(created_user))





@app.post("/generate-token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]




@app.post("/upload_image/", response_model=User)
async def upload_image(doc: bytes = File(), current_user: User = Depends(get_current_active_user)):
    content = io.BytesIO(doc)
    data = pytesseract.image_to_string(Image.open(content))
    # remove hyperlinks
    data = re.sub(r'https?:\/\/.\S+', "", data)
 
    # remove hashtags
    # only removing the hash # sign from the word
    data = re.sub(r'#', '', data)
    
    # remove old style retweet text "RT"
    data = re.sub(r'^RT[\s]+', '', data)


    data = data.replace('\n','')
    data = data.replace('\n','')
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=data)


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


@app.post("/generate-qr/{url}")
async def generate_qr(url: str):
    return {"message": "Nice"}


@app.post("/get-movie-recommendation/{genre}")
async def get_movie_recommendation(genre: str):
    return {"message": "Nice"}


@app.get("/get-playlist")
async def get_playlist(request: Request):
    client_host = request.client.host
    header = request.headers.raw
    ip = r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)
    return {"message": ip}

@app.get("/get-joke")
async def get_joke():
    return {"message": "Nice"}


@app.post("/get-account_details/{username}")
async def get_account_details(username: str):
    return {"message": "Nice"}