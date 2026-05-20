from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.quiz import QuizSubmitRequest, QuizSubmitResponse
from app.services.quiz_grader import grade_quiz


router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/{lesson_id}/submit", response_model=QuizSubmitResponse)
def submit_quiz(
    lesson_id: str,
    payload: QuizSubmitRequest,
    _current_user: User = Depends(get_current_user),
):
    result = grade_quiz(lesson_id, payload)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found.",
        )

    return result
