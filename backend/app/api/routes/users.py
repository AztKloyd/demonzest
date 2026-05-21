from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.security import hash_password
from app.db.session import get_db
from app.models.enums import LessonStatus
from app.models.lesson_progress import LessonProgress
from app.models.user import User
from app.schemas.user import UserCreate, UserProgressResponse, UserResponse
from app.services.content_loader import load_all_lesson_metadata


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserProgressResponse])
def list_users(
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    users = db.query(User).order_by(User.created_at.desc()).all()
    lesson_count = len(load_all_lesson_metadata())

    user_ids = [user.id for user in users]
    progress_rows = []
    if user_ids:
        progress_rows = (
            db.query(LessonProgress)
            .filter(LessonProgress.user_id.in_(user_ids))
            .all()
        )

    completed_by_user: dict[str, int] = {}
    for progress in progress_rows:
        if progress.status == LessonStatus.COMPLETED:
            completed_by_user[progress.user_id] = completed_by_user.get(progress.user_id, 0) + 1

    return [
        UserProgressResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            is_active=user.is_active,
            lesson_count=lesson_count,
            completed_count=completed_by_user.get(user.id, 0),
            progress_percent=round(completed_by_user.get(user.id, 0) / lesson_count * 100)
            if lesson_count > 0
            else 0,
        )
        for user in users
    ]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered.",
        )

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        name=payload.name,
        role=payload.role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
