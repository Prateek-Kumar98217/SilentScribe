from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core import database

class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    projects = relationship("Project", back_populates="owner", cascade="all, delete")