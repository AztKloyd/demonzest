from pydantic import BaseModel


class ProblemExample(BaseModel):
    input: str
    output: str
    explanation: str | None = None


class ProblemSummary(BaseModel):
    id: str
    title: str
    difficulty: str
    level: str
    order: int
    tags: list[str]
    time_limit_ms: int
    memory_limit_mb: int


class ProblemListResponse(BaseModel):
    problems: list[ProblemSummary]


class ProblemDetailResponse(ProblemSummary):
    body: str
    examples: list[ProblemExample]
