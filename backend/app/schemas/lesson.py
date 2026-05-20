from typing import Any

from pydantic import BaseModel

from app.schemas.progress import LessonProgressResponse


class LessonResponse(BaseModel):
    id: str
    course_id: str
    title: str
    description: str | None = None
    phase: int
    order: int
    level: str
    estimated_minutes: int
    tags: list[str]
    body: str
    quizzes: list[dict[str, Any]]
    progress: LessonProgressResponse | None = None
