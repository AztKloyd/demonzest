import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from app.models.enums import SubmissionStatus


def judge_sample_cases(
    language: str,
    code: str,
    examples: list[dict[str, Any]],
    time_limit_ms: int,
) -> dict[str, object]:
    if language.lower() != "python":
        return {
            "status": SubmissionStatus.RECEIVED,
            "score_percent": None,
            "runtime_ms": None,
            "feedback": "Only Python sample judging is available right now.",
        }

    if not examples:
        return {
            "status": SubmissionStatus.RECEIVED,
            "score_percent": None,
            "runtime_ms": None,
            "feedback": "No sample cases are defined for this problem.",
        }

    correct_count = 0
    total_runtime_ms = 0
    timeout_seconds = max(time_limit_ms / 1000, 1)

    with tempfile.TemporaryDirectory(prefix="demonzest-judge-") as temp_dir:
        source_path = Path(temp_dir) / "main.py"
        source_path.write_text(code, encoding="utf-8")

        for index, example in enumerate(examples, start=1):
            started_at = time.perf_counter()
            try:
                result = subprocess.run(
                    [sys.executable, "-I", str(source_path)],
                    input=ensure_final_newline(str(example["input"])),
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    timeout=timeout_seconds,
                    cwd=temp_dir,
                )
            except subprocess.TimeoutExpired:
                return build_result(
                    SubmissionStatus.TIME_LIMIT_EXCEEDED,
                    correct_count,
                    len(examples),
                    total_runtime_ms + time_limit_ms,
                    f"Sample {index} exceeded the time limit.",
                )

            runtime_ms = int((time.perf_counter() - started_at) * 1000)
            total_runtime_ms += runtime_ms

            if result.returncode != 0:
                stderr = result.stderr.strip() or "No error message."
                return build_result(
                    SubmissionStatus.RUNTIME_ERROR,
                    correct_count,
                    len(examples),
                    total_runtime_ms,
                    f"Sample {index} raised a runtime error: {stderr[:300]}",
                )

            expected = normalize_output(str(example["output"]))
            actual = normalize_output(result.stdout)
            if actual != expected:
                return build_result(
                    SubmissionStatus.WRONG_ANSWER,
                    correct_count,
                    len(examples),
                    total_runtime_ms,
                    f"Sample {index} failed. Expected '{expected}', got '{actual}'.",
                )

            correct_count += 1

    return build_result(
        SubmissionStatus.ACCEPTED,
        correct_count,
        len(examples),
        total_runtime_ms,
        "All sample cases passed.",
    )


def build_result(
    status: SubmissionStatus,
    correct_count: int,
    total_count: int,
    runtime_ms: int | None,
    feedback: str,
) -> dict[str, object]:
    return {
        "status": status,
        "score_percent": int(correct_count / total_count * 100) if total_count else None,
        "runtime_ms": runtime_ms,
        "feedback": feedback,
    }


def normalize_output(output: str) -> str:
    return output.replace("\r\n", "\n").strip()


def ensure_final_newline(value: str) -> str:
    return value if value.endswith("\n") else f"{value}\n"
