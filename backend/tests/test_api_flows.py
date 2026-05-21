from fastapi.testclient import TestClient


def test_login_and_me(client: TestClient, admin_headers: dict[str, str]):
    response = client.get("/api/me", headers=admin_headers)

    assert response.status_code == 200
    assert response.json()["email"] == "admin@example.com"


def test_roadmap_returns_courses(client: TestClient, admin_headers: dict[str, str]):
    response = client.get("/api/roadmap", headers=admin_headers)

    assert response.status_code == 200
    phases = response.json()["phases"]
    course_ids = [
        course["id"]
        for phase in phases
        for course in phase["courses"]
    ]
    assert "web-basics" in course_ids
    assert "javascript" in course_ids


def test_lesson_returns_body_and_public_quizzes(
    client: TestClient,
    admin_headers: dict[str, str],
):
    response = client.get("/api/lessons/web-001", headers=admin_headers)

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == "web-001"
    assert payload["body"]
    assert len(payload["quizzes"]) == 2
    assert "answer" not in payload["quizzes"][0]


def test_quiz_submit_grades_and_records_attempt(
    client: TestClient,
    admin_headers: dict[str, str],
):
    response = client.post(
        "/api/quiz/web-001/submit",
        headers=admin_headers,
        json={
            "answers": [
                {
                    "question_id": "web-001-q1",
                    "answer": "ブラウザ",
                },
                {
                    "question_id": "web-001-q2",
                    "answer": "サーバーはリクエストを処理して返す場所です。",
                },
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["attempt_id"]
    assert payload["lesson_id"] == "web-001"
    assert payload["total_questions"] == 2
    assert payload["auto_graded_count"] == 1
    assert payload["correct_count"] == 1
    assert payload["score_percent"] == 100


def test_admin_only_user_list(
    client: TestClient,
    admin_headers: dict[str, str],
    student_headers: dict[str, str],
):
    admin_response = client.get("/api/users", headers=admin_headers)
    student_response = client.get("/api/users", headers=student_headers)

    assert admin_response.status_code == 200
    assert admin_response.json()[0]["lesson_count"] > 0
    assert student_response.status_code == 403
