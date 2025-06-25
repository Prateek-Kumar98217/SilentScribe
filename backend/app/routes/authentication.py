from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.auth import Token
from app.services.auth import create_tokens, create_access_token, oauth2_refresh_schema, SECRET_KEY, ALGORITHM
import jwt
from jwt import PyJWTError
from app.repositories.user import get_user_by_email
from app.services.hashing import verify_password
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    tokens = create_tokens(user.email)
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_token(token: Annotated[str, Depends(oauth2_refresh_schema)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_access_token = create_access_token({"sub": user_email})
    return {
        "access_token": new_access_token,
        "refresh_token": token,  # or exclude this line if you prefer
        "token_type": "bearer"
    }
