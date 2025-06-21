from pydantic import BaseModel, validator
from typing import Literal

class CodeFileInput(BaseModel):
    file_name: str 
    file_type: Literal["py"]
    file_content: str

    @validator("file_name")
    def validate_file_name(cls, v):
        if not v.endswith(".py"):
            raise ValueError("Need python file")
        return v
    
    @validator("file_content")
    def validate_file_content(cls, v):
        if not v.strip():
            raise ValueError("File content cannot be empty")
        return v