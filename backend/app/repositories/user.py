from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def create_user(user: UserCreate, hashed_pw: str, db: Session)-> User:
    db_user = User(
        email = user.email,
        full_name = user.full_name,
        hashed_password = hashed_pw,
        is_active = True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user