from fastapi import Depends, HTTPException, status, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from app.repositories import project as project_repo
from app.dependencies.auth import get_current_user
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from app.core.database import get_db
from app.models.user import User

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

@router.post("/", response_model=ProjectOut)
def create(data: ProjectCreate, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    data.owner_id = user.id
    return project_repo.create_project(data, db)

@router.get("/", response_model=list[ProjectOut])
def get_all_projects(db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    projects=project_repo.get_projects_by_owner(user.id, db)
    if not projects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "You currently have no projects"
        )
    return projects

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    return verify_project_owner(project_id, db, user)

@router.patch("/{project_id}", response_model=ProjectOut)
def update(project_id: int, update_data: ProjectUpdate, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    project = verify_project_owner(project_id, db, user)
    return project_repo.update_project(project, update_data, db)

@router.delete("/{project_id}",response_model=None ,status_code=status.HTTP_204_NO_CONTENT)
def delete(project_id: int, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    project = verify_project_owner(project_id, db, user)
    return project_repo.delete_project(project, db)

#helper function for ownership checks
def verify_project_owner(project_id: int, db: Session, user: User):
    project = project_repo.get_project_by_id(project_id, db)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No project by id {project_id} found."
        )
    if project.owner_id!= user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=" You are not authorized to access this project."
        )
    return project