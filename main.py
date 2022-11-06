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
from passlib.hash import pbkdf2_sha256
import datetime
import qrcode


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
async def sign_up(full_name:str = Form(), email:str = Form(), password:str = Form(),):
    user = {
        'full_name': full_name,
        'email': email,
        'password': pbkdf2_sha256.hash(password),
        'expiration_date': (datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%Y-%m-%d"),
        'created_at': (datetime.datetime.now()).strftime("%Y-%m-%d")
    }
    is_present =  await db["user"].find_one({"email": email})
    if not is_present:
        new_user = await db["user"].insert_one(user)
        created_user = await db["user"].find_one({"_id": new_user.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Account created successfully! Welcome to your Aiden account")
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Email Address already in use. Please try login.")





@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"user": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}








@app.post("/upload_image/")
async def upload_image(doc: bytes = File(), current_user: User = Depends(get_current_user)):
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


@app.post("/generate-qr/")
async def generate_qr(url: str):
    # Encoding data using make() function
    img = qrcode.make(url)

    # Saving as an image file
    img.save('MyQRCode1.png')
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