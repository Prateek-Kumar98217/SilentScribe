from sqlalchemy.orm import Session
from app.models.codefile import CodeFile
from app.schemas.codefile import CodeFileCreate, CodeFileUpdate

def create_codefile(data: CodeFileCreate, db: Session)-> CodeFile:
    codefile=CodeFile(
        title=data.title,
        description=data.description,
        project_id=data.project_id
    )
    db.add(codefile)
    db.commit()
    db.refresh(codefile)
    return codefile

def get_codefile_by_id(codefile_id: int, db: Session)-> CodeFile:
    return db.get(CodeFile, codefile_id)

def get_codefiles_by_project_id(project_id: int, db: Session)-> list[CodeFile]:
    return db.query(CodeFile).filter(CodeFile.project_id==project_id).all()

def update_codefile(codefile: CodeFile, update_data: CodeFileUpdate, db: Session)-> CodeFile:
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(codefile, key, value)
    db.commit()
    db.refresh(codefile)
    return codefile

def delete_codefile(codefile: CodeFile, db: Session)-> None:
    db.delete(codefile)
    db.commit()