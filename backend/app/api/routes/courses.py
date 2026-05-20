from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.course import CourseDetailResponse, CourseListResponse
from app.services.content_loader import load_course, load_course_lessons_map, load_courses
from app.services.course_progress_service import attach_course_progress, attach_courses_progress


router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=CourseListResponse)
def get_courses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    courses = load_courses()
    course_lessons = load_course_lessons_map()
    courses = attach_courses_progress(db, current_user.id, courses, course_lessons)
    return CourseListResponse(courses=courses)


@router.get("/{course_id}", response_model=CourseDetailResponse)
def get_course(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    course = load_course(course_id)
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found.",
        )

    return attach_course_progress(db, current_user.id, course)
