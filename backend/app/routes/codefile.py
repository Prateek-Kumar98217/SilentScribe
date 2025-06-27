from fastapi import Depends, HTTPException, status, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from app.repositories import codefile as codefile_repo, project as project_repo
from app.dependencies.auth import get_current_user
from app.schemas.codefile import CodeFileCreate, CodeFileOut, CodeFileUpdate
from app.core.database import get_db
from app.models.user import User

router=APIRouter(
    prefix="/codefiles",
    tags=["Code Files"]
)

def verify_codefile_ownership(codefile_id: int, db: Session, user: User):
    codefile=codefile_repo.get_codefile_by_id(codefile_id, db)
    if not codefile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No codefile with id {codefile_id} not found."
        )
    project = project_repo.get_project_by_id(codefile.project_id, db)
    if not project or project.owner_id!=user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="File authorization fail."
        )
    return codefile

@router.post("/", response_model=CodeFileOut)
def create_codefile(data: CodeFileCreate, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    project=project_repo.get_project_by_id(data.project_id, db)
    if not project or project.owner_id!=user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to add this file to this project."
        )
    return codefile_repo.create_codefile(data, db)

@router.get("/{codefile_id}", response_model=CodeFileOut)
def get_codefile(codefile_id: int, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    return verify_codefile_ownership(codefile_id, db, user)

@router.get("/project/{project_id}", response_model=list[CodeFileOut])
def get_codefiles_by_project(project_id: int, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    project=project_repo.get_project_by_id(project_id, db)
    if not project or project.owner_id!=user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view code files for this project."
        )
    return codefile_repo.get_codefiles_by_project_id(project_id, db)

@router.patch("/{codefile_id}", response_model=CodeFileOut)
def update_codefile(codefile_id: int, update_data: CodeFileUpdate, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    codefile=verify_codefile_ownership(codefile_id, db, user)
    return codefile_repo.update_codefile(codefile, update_data, db)

@router.delete("/{codefile_id}", status_code=204)
def delete_codefile(codefile_id: int, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    codefile=verify_codefile_ownership(codefile_id, db, user)
    codefile_repo.delete_codefile(codefile, db)