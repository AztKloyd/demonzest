from pydantic import BaseModel


class CourseSummary(BaseModel):
    id: str
    title: str
    phase: int
    lesson_count: int


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


class CourseDetailResponse(BaseModel):
    id: str
    title: str
    phase: int
    lesson_count: int
    lessons: list[CourseLessonSummary]
