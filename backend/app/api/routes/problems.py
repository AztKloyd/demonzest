from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.problem import ProblemDetailResponse, ProblemListResponse
from app.services.problem_loader import load_problem, load_problem_summaries


router = APIRouter(prefix="/problems", tags=["problems"])


@router.get("", response_model=ProblemListResponse)
def get_problems(current_user: User = Depends(get_current_user)):
    return ProblemListResponse(problems=load_problem_summaries())


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
