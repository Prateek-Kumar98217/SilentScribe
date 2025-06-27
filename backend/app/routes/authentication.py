from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session
from app.schemas import user as user_schema, auth as auth_schema
from app.repositories import user as user_repo
from app.services import hashing, auth
from app.core.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

oauth2_access_schema = OAuth2PasswordBearer(tokenUrl="auth/login")
oauth2_refresh_schema = OAuth2PasswordBearer(tokenUrl="auth/refresh")

@router.post("/register", response_model=user_schema.UserOut)
def register_user(user: user_schema.UserCreate, db: Annotated[Session, Depends(get_db)]):
    if user_repo.get_user_by_email(user.email, db):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Email already registered"
        )
    hashed_pw = hashing.hash_password(user.password)
    return user_repo.create_user(user, hashed_pw, db)

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)])-> auth_schema.Token:
    user = user_repo.get_user_by_email(form_data.username, db)
    if not user or not hashing.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid credentials"
        )
    return auth.create_tokens(user.email)

@router.post("/refresh")
def refresh(token: Annotated[str, Depends(oauth2_refresh_schema)])-> auth_schema.Token:
    new_token = auth.refresh_access_token(token)
    if not new_token:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid refresh request"
        )
    return new_token