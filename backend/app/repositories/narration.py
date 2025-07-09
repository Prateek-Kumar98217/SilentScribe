from sqlalchemy.orm import Session
from app.models.narration import Narration
from app.schemas.api import NarrationBase


def create_narration( db: Session, script: NarrationBase) -> Narration:
    narration = Narration(
        target_type=script.target_type,
        content=script.content,
        style=script.style,
        block_id=script.block_id,
        test_id=script.test_id,
        refactored_id=script.refactored_id
    )
    db.add(narration)
    db.commit()
    db.refresh(narration)
    return narration


def get_narrations_by_block(db: Session, block_id: str) -> list[Narration]:
    return db.query(Narration).filter(Narration.block_id == block_id).all()


def get_narrations_by_test(db: Session, test_id: str) -> list[Narration]:
    return db.query(Narration).filter(Narration.test_id == test_id).all()


def get_narrations_by_refactored(db: Session, refactored_id: str) -> list[Narration]:
    return db.query(Narration).filter(Narration.refactored_id == refactored_id).all()
