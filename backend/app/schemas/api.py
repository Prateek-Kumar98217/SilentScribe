from pydantic import BaseModel, EmailStr
from typing import Literal


class UserBase(BaseModel):
    email: EmailStr
    full_name: str| None = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: str
    is_active: bool


class ProjectBase(BaseModel):
    title: str | None = None
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: str
    created_at: str
    owner_id: str


class CodeFileBase(BaseModel):
    name: str
    content: str


class CodeFileCreate(CodeFileBase):
    project_id: str


class CodeFileResponse(CodeFileBase):
    id: str
    created_at: str
    project_id: str


class CodeBlockResponse(BaseModel):
    id: str
    name: str | None = None
    code_type: Literal["function", "class", "module", "import", "variable"]
    docstring: str | None = None
    code: str
    file_id: str


class CodeReviewBase(BaseModel):
    quality_score: float
    requires_refactor: bool
    issues: list[str]
    comments: str | None = None

class CodeReviewResponse(CodeReviewBase):
    id: str
    block_id: str

class RefactorCodeBase(BaseModel):
    refactored_code: str
    change_summary: str | None = None

class RefactoredCodeResponse(RefactorCodeBase):
    id: str
    block_id: str

class GeneratedTestBase(BaseModel):
    test_code: str
    coverage_summary: str | None = None

class GeneratedTestResponse(GeneratedTestBase):
    id: str
    block_id: str


class NarrationBase(BaseModel):
    target_type: Literal["block", "test", "refactored"]
    content: str
    style: str | None = None
    block_id: str | None = None
    test_id: str | None = None
    refactored_id: str | None = None

class NarrationResponse(NarrationBase):
    id: str
    
