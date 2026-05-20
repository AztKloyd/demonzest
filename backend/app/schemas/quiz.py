from typing import Literal

from pydantic import BaseModel


QuestionType = Literal["fill_blank", "code_output", "short_answer"]


class QuizAnswerSubmit(BaseModel):
    question_id: str
    answer: str


class QuizSubmitRequest(BaseModel):
    answers: list[QuizAnswerSubmit]


class QuizResult(BaseModel):
    question_id: str
    type: QuestionType
    answer: str
    is_correct: bool | None
    correct_answer: str | None = None
    sample_answer: str | None = None
    explanation: str | None = None


class QuizSubmitResponse(BaseModel):
    attempt_id: str | None = None
    lesson_id: str
    total_questions: int
    auto_graded_count: int
    correct_count: int
    score_percent: int | None
    results: list[QuizResult]
