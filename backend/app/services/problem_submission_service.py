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
        feedback="提出を受け付けました。採点エンジンは次のステップで追加します。",
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


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
