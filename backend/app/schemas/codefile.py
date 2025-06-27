from pydantic import BaseModel
from datetime import datetime

class CodeFileBase(BaseModel):
    file_name: str
    file_content: str

class CodeFileCreate(BaseModel):
    pass

class CodeFileUpdate(BaseModel):
    file_name: str|None = None
    file_content: str|None = None

class CodeFileOut(BaseModel):
    id: int
    file_name: str
    file_content: str
    created_at: datetime