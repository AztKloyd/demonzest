from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import LessonStatus


class LessonProgressResponse(BaseModel):
    lesson_id: str
    status: LessonStatus
    progress_percent: int
    last_position: str | None = None
    last_viewed_at: datetime | None = None
    completed_at: datetime | None = None

    model_config = {
        "from_attributes": True,
    }


class LessonProgressUpdate(BaseModel):
    progress_percent: int = Field(ge=0, le=100)
    last_position: str | None = None

