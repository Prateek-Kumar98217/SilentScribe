from pydantic import BaseModel
from datetime import datetime

class ProjectBase(BaseModel):
    title: str
    description: str | None = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class ProjectOut(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }