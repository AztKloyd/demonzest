from sqlalchemy.orm import Session

from app.models.enums import LessonStatus
from app.models.lesson_progress import LessonProgress


def attach_course_progress(db: Session, user_id: str, course: dict) -> dict:
    lesson_ids = [lesson["id"] for lesson in course.get("lessons", [])]
    progress_by_lesson_id = get_progress_by_lesson_id(db, user_id, lesson_ids)

    completed_count = 0
    for lesson in course.get("lessons", []):
        progress = progress_by_lesson_id.get(lesson["id"])
        if progress is None:
            lesson["status"] = LessonStatus.NOT_STARTED.value
            lesson["progress_percent"] = 0
            continue

        lesson["status"] = progress.status.value
        lesson["progress_percent"] = progress.progress_percent
        if progress.status == LessonStatus.COMPLETED:
            completed_count += 1

    course["completed_count"] = completed_count
    course["progress_percent"] = calculate_percent(completed_count, course["lesson_count"])
    return course


def attach_courses_progress(
    db: Session,
    user_id: str,
    courses: list[dict],
    course_lessons: dict[str, list[dict]],
) -> list[dict]:
    all_lesson_ids = [
        lesson["id"]
        for lessons in course_lessons.values()
        for lesson in lessons
    ]
    progress_by_lesson_id = get_progress_by_lesson_id(db, user_id, all_lesson_ids)

    for course in courses:
        lessons = course_lessons.get(course["id"], [])
        completed_count = 0
        for lesson in lessons:
            progress = progress_by_lesson_id.get(lesson["id"])
            if progress is not None and progress.status == LessonStatus.COMPLETED:
                completed_count += 1

        course["completed_count"] = completed_count
        course["progress_percent"] = calculate_percent(completed_count, course["lesson_count"])

    return courses


def get_progress_by_lesson_id(
    db: Session,
    user_id: str,
    lesson_ids: list[str],
) -> dict[str, LessonProgress]:
    if not lesson_ids:
        return {}

    progress_list = (
        db.query(LessonProgress)
        .filter(
            LessonProgress.user_id == user_id,
            LessonProgress.lesson_id.in_(lesson_ids),
        )
        .all()
    )
    return {progress.lesson_id: progress for progress in progress_list}


def calculate_percent(completed_count: int, lesson_count: int) -> int:
    if lesson_count == 0:
        return 0
    return round(completed_count / lesson_count * 100)
