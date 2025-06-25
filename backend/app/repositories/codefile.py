from app.models import CodeFile
from backend.app.schemas.crud import CodeFileCreate, CodeFileUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def get_all_codefiles(db: Session, project_id: int) -> list[CodeFile]:
    """
    Retrieve all code files of a project from the database.
    """
    codefiles = db.query(CodeFile).filter(CodeFile.project_id == project_id).all()
    if not codefiles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No code files for the project found"
        )
    return codefiles

def get_codefile(db: Session, codefile_id: int)-> CodeFile:
    """
    Retrieve a code file by its ID.
    """
    codefile = db.get(CodeFile, codefile_id)
    if not codefile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Code file with ID {codefile_id} not found"
        )
    return codefile

def get_codefile_by_name(db: Session, project_id: int, file_name: str)->CodeFile:
    """
    Retrieve a code file by its name within a specific project.
    """
    codefile=db.query(CodeFile).filter(
        CodeFile.project_id == project_id,
        CodeFile.file_name == file_name
    ).first()
    if not codefile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Code file with name {file_name} not found in project {project_id}"
        )
    return codefile

def create_codefile(db:Session, codefile: CodeFileCreate) -> CodeFile:
    """
    Create a new code file for the project in the database
    """
    existing = db.query(CodeFile).filter(
        CodeFile.project_id == codefile.project_id,
        CodeFile.file_name == codefile.file_name
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Code file with name {codefile.file_name} already exists in project {codefile.project_id}"
        )
    db_codefile = CodeFile(
        file_name=codefile.file_name,
        file_content=codefile.file_content,
        project_id=codefile.project_id
    )
    db.add(db_codefile)
    db.commit()
    db.refresh(db_codefile)
    return db_codefile

def update_codefile(db:Session, codefile_id: int, update_data: CodeFileUpdate) -> CodeFile:
    """
    Update a code file of the project in database
    """
    codefile = db.get(CodeFile, codefile_id)
    if not codefile:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Code file with ID {codefile_id} not found"
        )
    for key, value in update_data.dict(exclude_unset =True).items():
        setattr(codefile, key, value)
    db.commit()
    db.refresh(codefile)
    return codefile

def delete_codefile(db:Session, codefile_id: int)-> None:
    """
    Delete a code file of the project from the database
    """
    codefile = db.get(CodeFile, codefile_id)
    if not codefile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Code file with ID {codefile_id} not found"
        )
    db.delete(codefile)
    db.commit()
    return None