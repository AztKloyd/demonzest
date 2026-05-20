from app.schemas.quiz import QuizSubmitRequest
from app.services.content_loader import load_lesson_quizzes


AUTO_GRADED_TYPES = {"fill_blank", "code_output"}


def grade_quiz(lesson_id: str, payload: QuizSubmitRequest) -> dict | None:
    quizzes = load_lesson_quizzes(lesson_id)
    if quizzes is None:
        return None

    answer_by_question_id = {
        answer.question_id: answer.answer
        for answer in payload.answers
    }

    results = []
    auto_graded_count = 0
    correct_count = 0

    for quiz in quizzes:
        question_id = quiz["id"]
        question_type = quiz["type"]
        user_answer = answer_by_question_id.get(question_id, "")

        result = {
            "question_id": question_id,
            "type": question_type,
            "answer": user_answer,
            "is_correct": None,
            "correct_answer": None,
            "sample_answer": None,
            "explanation": quiz.get("explanation"),
        }

        if question_type in AUTO_GRADED_TYPES:
            auto_graded_count += 1
            correct_answer = str(quiz.get("answer", ""))
            is_correct = normalize_answer(user_answer) == normalize_answer(correct_answer)
            if is_correct:
                correct_count += 1

            result["is_correct"] = is_correct
            result["correct_answer"] = correct_answer

        if question_type == "short_answer":
            result["sample_answer"] = quiz.get("sampleAnswer")

        results.append(result)

    score_percent = None
    if auto_graded_count > 0:
        score_percent = round(correct_count / auto_graded_count * 100)

    return {
        "lesson_id": lesson_id,
        "total_questions": len(quizzes),
        "auto_graded_count": auto_graded_count,
        "correct_count": correct_count,
        "score_percent": score_percent,
        "results": results,
    }


def normalize_answer(value: str) -> str:
    return value.strip().lower()
