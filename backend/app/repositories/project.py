from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

def create_project(data: ProjectCreate, db: Session)-> Project:
    db_project = Project(
        title = data.title,
        description = data.description,
        owner_id = data.owner_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_project_by_id(project_id: int, db: Session)-> Project:
    return db.get(Project, project_id)

def get_projects_by_owner(owner_id: int, db: Session)-> list[Project]:
    return db.query(Project).filter(Project.owner_id == owner_id).all()

def update_project(project: Project, update_data: ProjectUpdate, db: Session)-> Project:
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

def delete_project(project: Project, db: Session)-> None:
    db.delete(project)
    db.commit()

