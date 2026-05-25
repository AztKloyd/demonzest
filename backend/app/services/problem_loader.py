from pathlib import Path
from typing import Any

from app.services.content_loader import get_content_root, split_frontmatter


def get_problem_root() -> Path:
    return get_content_root() / "problems"


def load_problem(problem_id: str) -> dict[str, Any] | None:
    for markdown_path in iter_problem_files():
        raw = markdown_path.read_text(encoding="utf-8")
        metadata, body = split_frontmatter(raw)
        if metadata.get("id") == problem_id:
            return build_problem_response(metadata, body)
    return None


def load_problem_summaries() -> list[dict[str, Any]]:
    problems: list[dict[str, Any]] = []
    for markdown_path in iter_problem_files():
        raw = markdown_path.read_text(encoding="utf-8")
        metadata, _body = split_frontmatter(raw)
        if metadata.get("id"):
            problems.append(build_problem_summary(metadata))

    return sorted(problems, key=lambda problem: problem["order"])


def iter_problem_files() -> list[Path]:
    problem_root = get_problem_root()
    if not problem_root.exists():
        return []
    return list(problem_root.glob("*.md"))


def build_problem_summary(metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": metadata["id"],
        "title": metadata["title"],
        "difficulty": metadata["difficulty"],
        "level": metadata["level"],
        "order": metadata["order"],
        "tags": metadata.get("tags", []),
        "time_limit_ms": metadata["timeLimitMs"],
        "memory_limit_mb": metadata["memoryLimitMb"],
    }


def build_problem_response(metadata: dict[str, Any], body: str) -> dict[str, Any]:
    problem = build_problem_summary(metadata)
    problem["body"] = body.strip()
    problem["examples"] = metadata.get("examples", [])
    return problem
