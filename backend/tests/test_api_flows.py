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


def test_problem_list_and_detail(client: TestClient, admin_headers: dict[str, str]):
    list_response = client.get("/api/problems", headers=admin_headers)

    assert list_response.status_code == 200
    problems = list_response.json()["problems"]
    assert problems[0]["id"] == "algo-001"
    assert problems[0]["time_limit_ms"] == 1000

    detail_response = client.get("/api/problems/algo-001", headers=admin_headers)

    assert detail_response.status_code == 200
    payload = detail_response.json()
    assert payload["title"] == "A + B"
    assert payload["body"]
    assert payload["examples"][0]["input"] == "1 2"


def test_problem_submission_is_saved(client: TestClient, admin_headers: dict[str, str]):
    submit_response = client.post(
        "/api/problems/algo-001/submissions",
        headers=admin_headers,
        json={
            "language": "Python",
            "code": "a, b = map(int, input().split())\nprint(a + b)",
        },
    )

    assert submit_response.status_code == 200
    payload = submit_response.json()
    assert payload["problem_id"] == "algo-001"
    assert payload["language"] == "Python"
    assert payload["status"] == "received"

    list_response = client.get(
        "/api/problems/algo-001/submissions",
        headers=admin_headers,
    )

    assert list_response.status_code == 200
    submissions = list_response.json()["submissions"]
    assert len(submissions) == 1
    assert submissions[0]["id"] == payload["id"]


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
