from datetime import datetime, timedelta
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, PyJWTError
from app.repositories import user as user_repo
from app.schemas.auth import Token
from ..config import settings

def create_access_token(data: dict)-> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict)-> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_tokens(email: str)-> Token:
    payload = {"sub": email}
    return{
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
        "token_type": "bearer"
    }

def refresh_access_token(token: str)-> Token:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email = payload.get("sub")
        if not user_email:
            return False
    except (ExpiredSignatureError, InvalidTokenError):
        return False
    new_access = create_access_token({"sub": user_email})
    return{
        "access_token": new_access,
        "refresh_token": token,
        "token_type": "bearer"
    }
