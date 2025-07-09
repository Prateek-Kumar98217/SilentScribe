from sqlalchemy.orm import Session
from app.models import User
from app.schemas.api import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate, hashed_pw: str) -> User:
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_pw,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
