from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.progress import LessonProgressResponse, LessonProgressUpdate
from app.services.progress_service import complete_lesson, update_progress


router = APIRouter(prefix="/progress", tags=["progress"])


@router.put("/{lesson_id}", response_model=LessonProgressResponse)
def put_progress(
    lesson_id: str,
    payload: LessonProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_progress(
        db=db,
        user_id=current_user.id,
        lesson_id=lesson_id,
        progress_percent=payload.progress_percent,
        last_position=payload.last_position,
    )


@router.post("/{lesson_id}/complete", response_model=LessonProgressResponse)
def post_complete_lesson(
    lesson_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return complete_lesson(db=db, user_id=current_user.id, lesson_id=lesson_id)
