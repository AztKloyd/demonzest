from sqlalchemy.orm import Session

from app.models.enums import SubmissionStatus
from app.models.problem_submission import ProblemSubmission


def create_submission(
    db: Session,
    user_id: str,
    problem_id: str,
    language: str,
    code: str,
) -> ProblemSubmission:
    submission = ProblemSubmission(
        user_id=user_id,
        problem_id=problem_id,
        language=language,
        code=code,
        status=SubmissionStatus.RECEIVED,
        feedback="Submission received. Judge execution will be added later.",
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


def attach_submission_stats(
    db: Session,
    user_id: str,
    problems: list[dict[str, object]],
) -> list[dict[str, object]]:
    problem_ids = [str(problem["id"]) for problem in problems]
    if not problem_ids:
        return problems

    submissions = (
        db.query(ProblemSubmission)
        .filter(
            ProblemSubmission.user_id == user_id,
            ProblemSubmission.problem_id.in_(problem_ids),
        )
        .order_by(ProblemSubmission.submitted_at.desc())
        .all()
    )

    stats: dict[str, dict[str, object]] = {}
    for submission in submissions:
        problem_stats = stats.setdefault(
            submission.problem_id,
            {
                "submission_count": 0,
                "latest_status": submission.status.value,
                "last_submitted_at": submission.submitted_at.isoformat(),
            },
        )
        problem_stats["submission_count"] = int(problem_stats["submission_count"]) + 1

    for problem in problems:
        problem.update(
            stats.get(
                str(problem["id"]),
                {
                    "submission_count": 0,
                    "latest_status": None,
                    "last_submitted_at": None,
                },
            )
        )

    return problems


def list_user_submissions(
    db: Session,
    user_id: str,
    problem_id: str,
) -> list[ProblemSubmission]:
    return (
        db.query(ProblemSubmission)
        .filter(
            ProblemSubmission.user_id == user_id,
            ProblemSubmission.problem_id == problem_id,
        )
        .order_by(ProblemSubmission.submitted_at.desc())
        .all()
    )


def serialize_submission(submission: ProblemSubmission) -> dict[str, object]:
    return {
        "id": submission.id,
        "problem_id": submission.problem_id,
        "language": submission.language,
        "status": submission.status.value,
        "score_percent": submission.score_percent,
        "runtime_ms": submission.runtime_ms,
        "memory_kb": submission.memory_kb,
        "feedback": submission.feedback,
        "submitted_at": submission.submitted_at.isoformat(),
    }
