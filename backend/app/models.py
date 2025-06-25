from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable = False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now().isoformat())

    projects = relationship("Project", back_populates = "owner")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable = False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String, nullable=True)

    owner = relationship("User", back_populates="projects")
    files = relationship("CodeFiles", back_populates ="project")

class CodeFile(Base):
    __tablename__ = "code_files"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_content = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    created_at = Column(DateTime, default=datetime.now().isoformat())
    
    project = relationship("Project", back_populates="files")
    code_blocks = relationship("CodeBlock", back_populates="code_file")

class CodeBlock(Base):
    __tablename__ = "code_blocks"

    id = Column(Integer, primary_key=True, index=True)
    code_type = Column(String, nullable=False)
    name = Column(String, nullable=True)
    lineno = Column(Integer)
    col_offset = Column(Integer)
    end_lineno = Column(Integer)
    end_col_offset = Column(Integer)
    docstring = Column(String, nullable=True)
    used_names = Column(JSON, default = [])
    args = Column(JSON, default = [])
    returns = Column(String, nullable=True)
    code = Column(Text, nullable=False)
    file_id = Column(Integer, ForeignKey('code_files.id'))

    code_file = relationship("CodeFiles", back_populates="code_blocks")
    narration = relationship("Narration", back_populates="code_block")

class Narration(Base):
    __tablename__ ="narrations"

    id = Column(Integer, primary_key=True, index=True)
    script = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now().isoformat())
    code_block_id = Column(Integer, ForeignKey('code_blocks.id'))

    code_block = relationship("CodeBlock", back_populates="narration")
