from collections import defaultdict

from sqlalchemy.orm import Session

from app.services.content_loader import get_course_order, load_course_lessons_map, load_courses
from app.services.course_progress_service import attach_courses_progress


PHASE_TITLES = {
    1: "Foundation",
    2: "Frontend and data basics",
    3: "Backend practice",
    4: "Japanese development practice",
    5: "Certifications / Career",
}


def load_roadmap(db: Session, user_id: str) -> dict:
    courses = load_courses()
    course_lessons = load_course_lessons_map()
    courses = attach_courses_progress(db, user_id, courses, course_lessons)

    courses_by_phase = defaultdict(list)
    for course in courses:
        courses_by_phase[course["phase"]].append(course)

    phases = []
    for phase_id in sorted(courses_by_phase):
        phases.append(
            {
                "id": phase_id,
                "title": PHASE_TITLES.get(phase_id, f"Phase {phase_id}"),
                "courses": sorted(
                    courses_by_phase[phase_id],
                    key=lambda course: get_course_order(course["id"]),
                ),
            }
        )

    return {"phases": phases}
