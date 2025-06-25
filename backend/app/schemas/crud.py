from pydantic import BaseModel
from datetime import datetime

# User schema definations
class UserBase(BaseModel):
    email: str
    
class UserCreate(UserBase):
    full_name: str
    password: str

class UserUpdate(BaseModel):
    full_name: str | None = None
    password = str | None = None
    is_active: bool | None = None

class UserOut(UserBase):
    id: int
    full_name: str
    is_active: bool

# Project schema definitions    
class ProjectBase(BaseModel):
    title: str
    description: str | None = None

class ProjectCreate(ProjectBase):
    owner_id: int

class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
class ProjectOut(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime

# CodeFile schema definitions
class CodeFileBase(BaseModel):
    file_name: str
    file_content: str

class CodeFileCreate(CodeFileBase):
    project_id: int

class CodeFileUpdate(BaseModel):
    file_name: str | None = None
    file_content: str | None = None
class CodeFileOut(CodeFileBase):
    id: int
    project_id: int
    created_at: datetime

# CodeBlock schema definitions
class CodeBlockBase(BaseModel):
    code_type: str
    name: str | None = None
    lineno: int | None = None
    col_offset: int | None = None
    end_lineno: int | None = None
    end_col_offset: int | None = None
    docstring: str | None = None
    used_names: list[str] = []
    args: list[str] = []
    returns: str | None = None
    code: str

class CodeBlockOut(CodeBlockBase):
    id: int
    file_id: int

# Narration schema definitions
class NarrationBase(BaseModel):
    script: str

class NarrationCreate(NarrationBase):
    code_block_id: int

class NarrationOut(NarrationBase):
    id: int
    code_block_id: int
    created_at: datetime
