from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.problem import (
    ProblemDetailResponse,
    ProblemListResponse,
    ProblemSubmissionCreateRequest,
    ProblemSubmissionListResponse,
    ProblemSubmissionResponse,
)
from app.services.problem_loader import load_problem, load_problem_summaries
from app.services.problem_submission_service import (
    attach_submission_stats,
    create_submission,
    list_user_submissions,
    serialize_submission,
)
from app.services.sample_judge import judge_sample_cases


router = APIRouter(prefix="/problems", tags=["problems"])


@router.get("", response_model=ProblemListResponse)
def get_problems(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    problems = attach_submission_stats(db, current_user.id, load_problem_summaries())
    return ProblemListResponse(problems=problems)


@router.get("/{problem_id}", response_model=ProblemDetailResponse)
def get_problem(
    problem_id: str,
    current_user: User = Depends(get_current_user),
):
    problem = load_problem(problem_id)
    if problem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found.",
        )
    return problem


@router.get("/{problem_id}/submissions", response_model=ProblemSubmissionListResponse)
def get_problem_submissions(
    problem_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    problem = load_problem(problem_id)
    if problem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found.",
        )

    submissions = list_user_submissions(db, current_user.id, problem_id)
    return ProblemSubmissionListResponse(
        submissions=[serialize_submission(submission) for submission in submissions]
    )


@router.post("/{problem_id}/submissions", response_model=ProblemSubmissionResponse)
def submit_problem(
    problem_id: str,
    payload: ProblemSubmissionCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    problem = load_problem(problem_id)
    if problem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found.",
        )

    if not payload.code.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code is required.",
        )

    judge_result = judge_sample_cases(
        language=payload.language,
        code=payload.code,
        examples=problem["examples"],
        time_limit_ms=problem["time_limit_ms"],
    )
    submission = create_submission(
        db=db,
        user_id=current_user.id,
        problem_id=problem_id,
        language=payload.language,
        code=payload.code,
        status=judge_result["status"],
        score_percent=judge_result["score_percent"],
        runtime_ms=judge_result["runtime_ms"],
        feedback=judge_result["feedback"],
    )
    return serialize_submission(submission)
