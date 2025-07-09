from sqlalchemy.orm import Session
from app.models import GeneratedTest
from app.schemas.api import GeneratedTestBase


def create_test( db: Session, test: GeneratedTestBase) -> GeneratedTest:
    test = GeneratedTest(
        block_id=test.block_id,
        test_code=test.test_code,
        coverage_summary=test.coverage_summary
    )
    db.add(test)
    db.commit()
    db.refresh(test)
    return test


def get_test_by_block(db: Session, block_id: str) -> GeneratedTest | None:
    return db.query(GeneratedTest).filter(GeneratedTest.block_id == block_id).first()
