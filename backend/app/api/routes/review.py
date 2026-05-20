from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.wrong_answer import WrongAnswer
from app.schemas.review import WrongAnswerItem, WrongAnswerListResponse
from app.services.content_loader import load_lesson_metadata, load_lesson_quiz


router = APIRouter(prefix="/review", tags=["review"])


@router.get("/wrong-answers", response_model=WrongAnswerListResponse)
def list_wrong_answers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    wrong_answers = (
        db.query(WrongAnswer)
        .filter(
            WrongAnswer.user_id == current_user.id,
            WrongAnswer.resolved_at.is_(None),
        )
        .order_by(WrongAnswer.last_wrong_at.desc())
        .all()
    )

    items = []
    for wrong_answer in wrong_answers:
        metadata = load_lesson_metadata(wrong_answer.lesson_id)
        quiz = load_lesson_quiz(wrong_answer.lesson_id, wrong_answer.question_id)
        items.append(
            WrongAnswerItem(
                lesson_id=wrong_answer.lesson_id,
                lesson_title=metadata.get("title") if metadata else None,
                question_id=wrong_answer.question_id,
                question_type=wrong_answer.question_type,
                question=quiz.get("question") if quiz else None,
                wrong_count=wrong_answer.wrong_count,
                last_wrong_answer=wrong_answer.last_wrong_answer,
                last_wrong_at=wrong_answer.last_wrong_at,
                resolved_at=wrong_answer.resolved_at,
            )
        )

    return WrongAnswerListResponse(items=items)
