import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.token import TokenDB
from models.user import UsersDB
from schemas.token import TokenData
from passlib.context import CryptContext
from configs.database import get_db
from passlib.handlers.django import django_pbkdf2_sha256
from daos.token_dao import TokenCRUD


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="tokens", scheme_name="JWT")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_EXPIRE_DAYS = 60

def hash_password(password: str):
    return django_pbkdf2_sha256.hash(password)

def verify_password(password, encrypted_pasword):
    return django_pbkdf2_sha256.verify(password, encrypted_pasword)


def get_user(username: str):
    db = next(get_db())
    return db.query(UsersDB).where(UsersDB.username == username).one_or_none()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = "Null"):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        #expire = datetime.utcnow() + timedelta(minutes=1)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username == "Null":
            raise credentials_exception
            
        db = next(get_db())

        token = db.query(TokenDB).filter(TokenDB.token == token).first()

        if not token:
            db.close()
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError:
        if not token:
            raise credentials_exception
        try:
            db = next(get_db())
            token_temp = TokenCRUD(db).get_token_by_token(token)
            if token_temp:
                TokenCRUD(db).delete_token(token)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tu token ha expirado, por favor inicia sesión nuevamente",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tu token ha expirado, por favor inicia sesión nuevamente",
                headers={"WWW-Authenticate": "Bearer"},
            )
    user = get_user(username=token_data.username)
    if not user:
        db.close()
        raise credentials_exception

    db.close()
    return user


async def get_current_active_user(current_user: UsersDB = Depends(get_current_user)):
    # if current_user.disabled:
    #    raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
