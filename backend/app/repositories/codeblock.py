from sqlalchemy.orm import Session
from app.models import CodeBlock


def delete_blocks_by_file(db: Session, file_id: str) -> None:
    db.query(CodeBlock).filter(CodeBlock.file_id == file_id).delete()
    db.commit()


def create_codeblocks_bulk(db: Session, blocks: list[dict]) -> list[CodeBlock]:
    db_blocks = [CodeBlock(**block) for block in blocks]
    db.add_all(db_blocks)
    db.commit()
    return db_blocks


def get_blocks_by_file(db: Session, file_id: str) -> list[CodeBlock]:
    return db.query(CodeBlock).filter(CodeBlock.file_id == file_id).all()
