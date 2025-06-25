from app.models import Project
from backend.app.schemas.crud import ProjectCreate, ProjectUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def get_all_projects(db: Session, owner_id: int) -> list[Project]:
    """
    Retrieve all projects of a user from the database.
    """
    projects = db.query(Project).filter(Project.owner_id == owner_id).all()
    if not projects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No project of the user found"
        )
    return projects

def get_project(db: Session, project_id: int)-> Project:
    """
    Retrieve a project by its ID.
    """
    project_data = db.get(Project, project_id)
    if not project_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    return project_data

def create_project(db:Session, project: ProjectCreate) -> Project:
    """
    Create a new project for the user in the database
    """
    db_project = Project(
        title=project.title,
        description=project.description,
        owner_id=project.owner_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db:Session, project_id: int, update_data: ProjectUpdate) -> Project:
    """
    Update a project of the user in database
    """
    project_data = db.get(Project, project_id)
    if not project_data:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Project with ID {project_id} not found"
        )
    for key, value in update_data.dict(exclude_unset =True).items():
        setattr(project_data, key, value)
    db.commit()
    db.refresh(project_data)
    return project_data

def delete_project(db:Session, project_id: int)-> None:
    """
    Delete a project of the user from the database
    """
    project_data = db.get(Project, project_id)
    if not project_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    db.delete(project_data)
    db.commit()
    return None