from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.quiz import QuizSubmitRequest, QuizSubmitResponse
from app.services.quiz_grader import grade_quiz
from app.services.quiz_result_service import save_quiz_result


router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/{lesson_id}/submit", response_model=QuizSubmitResponse)
def submit_quiz(
    lesson_id: str,
    payload: QuizSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = grade_quiz(lesson_id, payload)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found.",
        )

    attempt_id = save_quiz_result(db, current_user.id, result)
    result["attempt_id"] = attempt_id

    return result
