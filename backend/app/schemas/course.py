from pydantic import BaseModel


class CourseSummary(BaseModel):
    id: str
    title: str
    phase: int
    lesson_count: int
    completed_count: int = 0
    progress_percent: int = 0


class CourseListResponse(BaseModel):
    courses: list[CourseSummary]


class CourseLessonSummary(BaseModel):
    id: str
    title: str
    description: str | None = None
    order: int
    level: str
    estimated_minutes: int
    tags: list[str]
    status: str = "not_started"
    progress_percent: int = 0


class CourseDetailResponse(BaseModel):
    id: str
    title: str
    phase: int
    lesson_count: int
    completed_count: int = 0
    progress_percent: int = 0
    lessons: list[CourseLessonSummary]
