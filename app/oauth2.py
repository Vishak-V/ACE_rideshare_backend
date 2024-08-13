from fastapi import HTTPException, Depends, status
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas,database,models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str=payload.get("userId")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(userId=id)
        return token_data
    except JWTError:
        raise credentials_exception
        return None
    
def get_current_user(token: str = Depends(oauth2_scheme),db: Session=Depends(database.get_db)):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token=verify_token(token, credentialsException)

    user=db.query(models.User).filter(models.User.id==token.userId).first()
    return user
