from app.models import User
from backend.app.schemas.crud import UserCreate, UserUpdate
from app.services import hashing
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def get_all_users(db: Session) -> list[User]:
    """
    Retrieve all users from the database.
    """
    users = db.query(User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    return users

def get_user(db: Session, user_id: int)-> User:
    """
    Retrieve a user by their ID.
    """
    user_data = db.get(User, user_id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user_data

def get_user_by_email(db: Session, email: str) -> User:
    """
    Retrieve a user by their email.
    """
    user_data = db.query(User).filter(User.email == email).first()
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found"
        )
    return user_data

def create_user(db:Session, user: UserCreate) -> User:
    """
    Create a new user in the database
    """
    db_user = User(
        email=user.email,
        hashed_password=hashing.hash_password(user.password),
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db:Session, user_id: int, update_data: UserUpdate) -> User:
    """
    Update a existing user in database
    """
    user_data = db.get(User, user_id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    for key, value in update_data.dict(exclude_unset=True).items():
        if key == "password":
            value = hashing.hash_password(value)
        setattr(user_data, key, value)
    db.commit()
    db.refresh(user_data)
    return user_data

def delete_user(db:Session, user_id: int)-> None:
    """
    Delete a user from the database
    """
    user_data = db.get(User, user_id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    db.delete(user_data)
    db.commit()
    return None