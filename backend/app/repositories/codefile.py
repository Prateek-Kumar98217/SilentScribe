from sqlalchemy.orm import Session
from app.models import CodeFile
from app.schemas.api import CodeFileCreate


def create_codefile(db: Session, data: CodeFileCreate) -> CodeFile:
    db_file = CodeFile(
        name=data.name,
        content=data.content,
        project_id=data.project_id
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_codefile(db: Session, file_id: str) -> CodeFile | None:
    return db.get(CodeFile, file_id)


def get_codefiles_by_project(db: Session, project_id: str) -> list[CodeFile]:
    return db.query(CodeFile).filter(CodeFile.project_id == project_id).all()


def delete_codefile(db: Session, file: CodeFile) -> None:
    db.delete(file)
    db.commit()
