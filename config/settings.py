from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import pytesseract
import os



SECRET_KEY = "d485e9906982b74d8a1efa5e5b7f5478f07aebeded767485a700aed322df737d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600
MONGO_DB_URL = os.getenv("MONGO_DB_URL")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Setting the path to the tesseract executable.
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH")



# Creating a password context and a oauth2_scheme.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

