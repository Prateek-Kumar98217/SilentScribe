import jwt
from fastapi import HTTPException, status, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from jwt.exceptions import PyJWTError
from app.repositories import user as user_repo
from app.routes.authentication import oauth2_access_schema
from app.core.database import get_db
from app.models.user import User
from ..config import settings

def get_current_user(token: Annotated[str, Depends(oauth2_access_schema)], db: Annotated[Session, Depends(get_db)])-> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid Token"
            )
    except PyJWTError:
        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid Token"
            )
    user = user_repo.get_user_by_email(email, db)
    if not user:
        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "User not found"
            )
    return user