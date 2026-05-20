import re
from pathlib import Path
from typing import Any

import yaml

from app.core.config import settings


FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
QUIZ_BLOCK_PATTERN = re.compile(r"```quiz\s*\n(.*?)\n```", re.DOTALL)


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


def load_lesson_metadata(lesson_id: str) -> dict[str, Any] | None:
    content_root = get_content_root()
    for markdown_path in content_root.rglob("*.md"):
        raw = markdown_path.read_text(encoding="utf-8")
        metadata, _body = split_frontmatter(raw)
        if metadata.get("id") == lesson_id:
            return metadata
    return None


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
