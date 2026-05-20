from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.models.enums import QuestionType
from app.models.quiz_answer import QuizAnswer
from app.models.quiz_attempt import QuizAttempt
from app.models.wrong_answer import WrongAnswer


def save_quiz_result(db: Session, user_id: str, result: dict[str, Any]) -> str:
    attempt = QuizAttempt(
        user_id=user_id,
        lesson_id=result["lesson_id"],
        total_questions=result["total_questions"],
        auto_graded_count=result["auto_graded_count"],
        correct_count=result["correct_count"],
        score_percent=result["score_percent"],
    )
    db.add(attempt)
    db.flush()

    for answer_result in result["results"]:
        question_type = QuestionType(answer_result["type"])
        quiz_answer = QuizAnswer(
            attempt_id=attempt.id,
            question_id=answer_result["question_id"],
            question_type=question_type,
            user_answer=answer_result["answer"],
            correct_answer=answer_result["correct_answer"],
            is_correct=answer_result["is_correct"],
            feedback=answer_result["explanation"] or answer_result["sample_answer"],
        )
        db.add(quiz_answer)

        update_wrong_answer(db, user_id, result["lesson_id"], answer_result, question_type)

    db.commit()
    return attempt.id


def update_wrong_answer(
    db: Session,
    user_id: str,
    lesson_id: str,
    answer_result: dict[str, Any],
    question_type: QuestionType,
) -> None:
    if answer_result["is_correct"] is None:
        return

    wrong_answer = (
        db.query(WrongAnswer)
        .filter(
            WrongAnswer.user_id == user_id,
            WrongAnswer.question_id == answer_result["question_id"],
        )
        .first()
    )

    if answer_result["is_correct"]:
        if wrong_answer is not None and wrong_answer.resolved_at is None:
            wrong_answer.resolved_at = datetime.now(timezone.utc)
        return

    if wrong_answer is None:
        wrong_answer = WrongAnswer(
            user_id=user_id,
            lesson_id=lesson_id,
            question_id=answer_result["question_id"],
            question_type=question_type,
            last_wrong_answer=answer_result["answer"],
        )
        db.add(wrong_answer)
        return

    wrong_answer.wrong_count += 1
    wrong_answer.last_wrong_answer = answer_result["answer"]
    wrong_answer.last_wrong_at = datetime.now(timezone.utc)
    wrong_answer.resolved_at = None
