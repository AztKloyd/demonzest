from datetime import datetime

from pydantic import BaseModel

from app.models.enums import QuestionType


class WrongAnswerItem(BaseModel):
    lesson_id: str
    lesson_title: str | None = None
    question_id: str
    question_type: QuestionType
    question: str | None = None
    wrong_count: int
    last_wrong_answer: str | None = None
    last_wrong_at: datetime
    resolved_at: datetime | None = None


class WrongAnswerListResponse(BaseModel):
    items: list[WrongAnswerItem]
