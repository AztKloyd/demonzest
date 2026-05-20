from collections import defaultdict

from app.services.content_loader import load_courses


PHASE_TITLES = {
    1: "Web development overview",
    2: "Git / GitHub",
    3: "JavaScript",
    4: "TypeScript",
    5: "React",
    6: "API",
    7: "SQL / Database",
    8: "Python Backend",
    9: "Java / Spring",
    10: "Japanese development practice",
    11: "Certifications / Career",
}


def load_roadmap() -> dict:
    courses_by_phase = defaultdict(list)
    for course in load_courses():
        courses_by_phase[course["phase"]].append(course)

    phases = []
    for phase_id in sorted(courses_by_phase):
        phases.append(
            {
                "id": phase_id,
                "title": PHASE_TITLES.get(phase_id, f"Phase {phase_id}"),
                "courses": sorted(
                    courses_by_phase[phase_id],
                    key=lambda course: course["id"],
                ),
            }
        )

    return {"phases": phases}
