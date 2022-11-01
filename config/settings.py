from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import pytesseract
import os



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
MONGO_DB_URL = os.getenv("MONGO_DB_URL")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Setting the path to the tesseract executable.
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH")



# Creating a password context and a oauth2_scheme.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

