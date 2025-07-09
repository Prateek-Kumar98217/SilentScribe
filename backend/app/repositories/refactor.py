from sqlalchemy.orm import Session
from app.models import RefactoredCode
from app.schemas.api import RefactorCodeBase

def create_refactored_code(db: Session, refactor: RefactorCodeBase) -> RefactoredCode:
    refactor = RefactoredCode(
        block_id=refactor.block_id,
        refactored_code=refactor.refactored_code,
        change_summary=refactor.change_summary
    )
    db.add(refactor)
    db.commit()
    db.refresh(refactor)
    return refactor


def get_refactor_by_block(db: Session, block_id: str) -> RefactoredCode | None:
    return db.query(RefactoredCode).filter(RefactoredCode.block_id == block_id).first()
