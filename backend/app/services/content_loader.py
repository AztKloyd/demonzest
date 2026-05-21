import re
from pathlib import Path
from typing import Any

import yaml

from app.core.config import settings


FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
QUIZ_BLOCK_PATTERN = re.compile(r"```quiz\s*\n(.*?)\n```", re.DOTALL)

COURSE_ORDER = {
    "web-basics": 10,
    "git-github": 20,
    "javascript": 30,
    "typescript": 40,
    "react": 50,
    "api": 60,
    "sql-db": 70,
    "python-backend": 80,
    "java-spring": 90,
    "japan-dev-practice": 100,
    "certification": 110,
}

COURSE_TITLES = {
    "web-basics": "Web開発の全体像",
    "git-github": "Git / GitHub",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "react": "React",
    "api": "API",
    "sql-db": "SQL / Database",
    "python-backend": "Python Backend",
    "java-spring": "Java / Spring",
    "japan-dev-practice": "日本の開発実務",
    "certification": "資格 / キャリア",
}


def get_content_root() -> Path:
    backend_root = Path(__file__).resolve().parents[2]
    return (backend_root / settings.content_dir).resolve()


def load_lesson(lesson_id: str) -> dict[str, Any] | None:
    content_root = get_content_root()
    for markdown_path in content_root.rglob("*.md"):
        raw = markdown_path.read_text(encoding="utf-8")
        metadata, body = split_frontmatter(raw)
        if metadata.get("id") == lesson_id:
            return build_lesson_response(metadata, body)
    return None


def load_all_lesson_metadata() -> list[dict[str, Any]]:
    lessons: list[dict[str, Any]] = []
    content_root = get_content_root()
    for markdown_path in content_root.rglob("*.md"):
        raw = markdown_path.read_text(encoding="utf-8")
        metadata, _body = split_frontmatter(raw)
        if metadata.get("id"):
            lessons.append(metadata)

    return sorted(
        lessons,
        key=lambda lesson: (
            lesson.get("phase", 0),
            get_course_order(lesson.get("courseId", "")),
            lesson.get("order", 0),
        ),
    )


def load_courses() -> list[dict[str, Any]]:
    courses: dict[str, dict[str, Any]] = {}
    for lesson in load_all_lesson_metadata():
        course_id = lesson["courseId"]
        course = courses.setdefault(
            course_id,
            {
                "id": course_id,
                "title": get_course_title(course_id),
                "phase": lesson["phase"],
                "lesson_count": 0,
            },
        )
        course["lesson_count"] += 1
        course["phase"] = min(course["phase"], lesson["phase"])

    return sorted(
        courses.values(),
        key=lambda course: (course["phase"], get_course_order(course["id"])),
    )


def load_course(course_id: str) -> dict[str, Any] | None:
    lessons = [
        lesson
        for lesson in load_all_lesson_metadata()
        if lesson.get("courseId") == course_id
    ]
    if not lessons:
        return None

    lessons.sort(key=lambda lesson: lesson.get("order", 0))
    return {
        "id": course_id,
        "title": get_course_title(course_id),
        "phase": min(lesson["phase"] for lesson in lessons),
        "lesson_count": len(lessons),
        "lessons": [
            {
                "id": lesson["id"],
                "title": lesson["title"],
                "description": lesson.get("description"),
                "order": lesson["order"],
                "level": lesson["level"],
                "estimated_minutes": lesson["estimatedMinutes"],
                "tags": lesson.get("tags", []),
            }
            for lesson in lessons
        ],
    }


def load_course_lessons_map() -> dict[str, list[dict[str, Any]]]:
    lessons_by_course: dict[str, list[dict[str, Any]]] = {}
    for lesson in load_all_lesson_metadata():
        course_id = lesson["courseId"]
        lessons_by_course.setdefault(course_id, []).append(
            {
                "id": lesson["id"],
                "order": lesson["order"],
            }
        )

    for lessons in lessons_by_course.values():
        lessons.sort(key=lambda lesson: lesson["order"])

    return lessons_by_course


def load_lesson_metadata(lesson_id: str) -> dict[str, Any] | None:
    content_root = get_content_root()
    for markdown_path in content_root.rglob("*.md"):
        raw = markdown_path.read_text(encoding="utf-8")
        metadata, _body = split_frontmatter(raw)
        if metadata.get("id") == lesson_id:
            return metadata
    return None


def get_course_title(course_id: str) -> str:
    return COURSE_TITLES.get(course_id, course_id)


def get_course_order(course_id: str) -> int:
    return COURSE_ORDER.get(course_id, 999)


def load_lesson_quizzes(lesson_id: str) -> list[dict[str, Any]] | None:
    content_root = get_content_root()
    for markdown_path in content_root.rglob("*.md"):
        raw = markdown_path.read_text(encoding="utf-8")
        metadata, body = split_frontmatter(raw)
        if metadata.get("id") == lesson_id:
            return extract_private_quizzes(body)
    return None


def load_lesson_quiz(lesson_id: str, question_id: str) -> dict[str, Any] | None:
    quizzes = load_lesson_quizzes(lesson_id)
    if quizzes is None:
        return None

    for quiz in quizzes:
        if quiz.get("id") == question_id:
            public_quiz = dict(quiz)
            public_quiz.pop("answer", None)
            public_quiz.pop("sampleAnswer", None)
            public_quiz.pop("keywords", None)
            public_quiz.pop("explanation", None)
            return public_quiz
    return None


def split_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_PATTERN.match(raw)
    if match is None:
        return {}, raw

    metadata = yaml.safe_load(match.group(1)) or {}
    body = raw[match.end() :]
    return metadata, body


def build_lesson_response(metadata: dict[str, Any], body: str) -> dict[str, Any]:
    quizzes = extract_public_quizzes(body)
    body_without_quizzes = QUIZ_BLOCK_PATTERN.sub("", body).strip()

    return {
        "id": metadata["id"],
        "course_id": metadata["courseId"],
        "title": metadata["title"],
        "description": metadata.get("description"),
        "phase": metadata["phase"],
        "order": metadata["order"],
        "level": metadata["level"],
        "estimated_minutes": metadata["estimatedMinutes"],
        "tags": metadata.get("tags", []),
        "body": body_without_quizzes,
        "quizzes": quizzes,
    }


def extract_public_quizzes(body: str) -> list[dict[str, Any]]:
    quizzes: list[dict[str, Any]] = []
    for match in QUIZ_BLOCK_PATTERN.finditer(body):
        quiz = yaml.safe_load(match.group(1)) or {}
        quiz.pop("answer", None)
        quiz.pop("sampleAnswer", None)
        quiz.pop("keywords", None)
        quiz.pop("explanation", None)
        quizzes.append(quiz)
    return quizzes


def extract_private_quizzes(body: str) -> list[dict[str, Any]]:
    quizzes: list[dict[str, Any]] = []
    for match in QUIZ_BLOCK_PATTERN.finditer(body):
        quiz = yaml.safe_load(match.group(1)) or {}
        quizzes.append(quiz)
    return quizzes
