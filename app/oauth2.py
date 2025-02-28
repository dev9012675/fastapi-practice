import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends , HTTPException , status
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from . import schemas , models , database


load_dotenv()

SECRET_KEY =  os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    print(f'Access token expiry time:{expire}')
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme) , db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        print(f'JWT Payload:{payload}')
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except InvalidTokenError as error:
        print(error)
        raise credentials_exception
    user =  db.query(models.User).filter(models.User.id == token_data.id).first()
    if user is None:
        raise credentials_exception
    return user

