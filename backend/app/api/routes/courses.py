from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.course import CourseDetailResponse, CourseListResponse
from app.services.content_loader import load_course, load_courses


router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=CourseListResponse)
def get_courses(_current_user: User = Depends(get_current_user)):
    return CourseListResponse(courses=load_courses())


@router.get("/{course_id}", response_model=CourseDetailResponse)
def get_course(
    course_id: str,
    _current_user: User = Depends(get_current_user),
):
    course = load_course(course_id)
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found.",
        )

    return course
