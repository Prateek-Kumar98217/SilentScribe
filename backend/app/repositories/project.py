from sqlalchemy.orm import Session
from app.models import Project
from app.schemas.api import ProjectCreate


def create_project(db: Session, data: ProjectCreate, owner_id: str) -> Project:
    db_project = Project(
        title=data.title,
        description=data.description,
        owner_id=owner_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project_by_id(db: Session, project_id: str) -> Project | None:
    return db.get(Project, project_id)


def get_projects_by_owner(db: Session, owner_id: str) -> list[Project]:
    return db.query(Project).filter(Project.owner_id == owner_id).all()


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()
