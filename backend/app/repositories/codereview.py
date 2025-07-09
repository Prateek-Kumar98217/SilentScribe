from sqlalchemy.orm import Session
from app.models import CodeReview
from app.schemas.api import CodeReviewBase


def create_review(db: Session, block_id: str, review: CodeReviewBase) -> CodeReview:
    review = CodeReview(
        block_id=block_id,
        issues=review.issues,
        quality_score=review.quality_score,
        requires_refactor=review.requires_refactor,
        comments=review.comments
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def get_review_by_block(db: Session, block_id: str) -> CodeReview | None:
    return db.query(CodeReview).filter(CodeReview.block_id == block_id).first()
