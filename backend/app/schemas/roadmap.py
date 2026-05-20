from pydantic import BaseModel

from app.schemas.course import CourseSummary


class RoadmapPhase(BaseModel):
    id: int
    title: str
    courses: list[CourseSummary]


class RoadmapResponse(BaseModel):
    phases: list[RoadmapPhase]
