from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.enums import LessonStatus
from app.models.lesson_progress import LessonProgress


def get_progress(db: Session, user_id: str, lesson_id: str) -> LessonProgress | None:
    return (
        db.query(LessonProgress)
        .filter(
            LessonProgress.user_id == user_id,
            LessonProgress.lesson_id == lesson_id,
        )
        .first()
    )


def update_progress(
    db: Session,
    user_id: str,
    lesson_id: str,
    progress_percent: int,
    last_position: str | None,
) -> LessonProgress:
    progress = get_progress(db, user_id, lesson_id)
    now = datetime.now(timezone.utc)

    if progress is None:
        progress = LessonProgress(
            user_id=user_id,
            lesson_id=lesson_id,
        )
        db.add(progress)

    progress.progress_percent = progress_percent
    progress.last_position = last_position
    progress.last_viewed_at = now
    if progress.status != LessonStatus.COMPLETED:
        progress.status = LessonStatus.IN_PROGRESS

    db.commit()
    db.refresh(progress)
    return progress


def complete_lesson(db: Session, user_id: str, lesson_id: str) -> LessonProgress:
    progress = get_progress(db, user_id, lesson_id)
    now = datetime.now(timezone.utc)

    if progress is None:
        progress = LessonProgress(
            user_id=user_id,
            lesson_id=lesson_id,
        )
        db.add(progress)

    progress.status = LessonStatus.COMPLETED
    progress.progress_percent = 100
    progress.last_viewed_at = now
    progress.completed_at = now

    db.commit()
    db.refresh(progress)
    return progress
