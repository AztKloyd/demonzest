# demonzest

`demonzest` is a learning web application for junior developers who need to study practical development skills in Japanese.

This project is split into three main areas:

- `frontend`: Angular application for screens and user interaction.
- `backend`: FastAPI application for API, authentication, progress, and quiz records.
- `content`: Markdown lessons used as learning material.

## Current Stack

- Frontend: Angular, TypeScript, SCSS
- Backend: FastAPI, SQLAlchemy, Alembic
- Database: PostgreSQL
- Lesson content: Markdown files under `content/`

## Local URLs

- Frontend: `http://localhost:4200`
- Backend API: `http://127.0.0.1:8000/api`
- API health check: `http://127.0.0.1:8000/api/health`

## Start Backend

Open PowerShell:

```powershell
cd C:\Users\HwangSangyon\Documents\Codex\2026-05-15\new-chat\learning\demonzest\backend
.\.venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000 --reload
```

Keep this terminal open.

## Start Frontend

Open another PowerShell:

```powershell
cd C:\Users\HwangSangyon\Documents\Codex\2026-05-15\new-chat\learning\demonzest\frontend
npm.cmd run start -- --host 127.0.0.1 --port 4200
```

Then open:

```text
http://localhost:4200
```

## Dev Login

```text
admin@example.com
admin-password123
```

If this account does not exist locally, run the admin seed script from `backend/` after setting `.env`.

```powershell
.\.venv\Scripts\python.exe scripts\seed_admin.py
```

## What Works Now

- Login with JWT stored in browser local storage
- Dashboard progress summary
- Roadmap and course detail pages
- Lesson reading page with formatted Markdown-like content
- Lesson completion
- Quiz answer submission and grading result display
- Wrong answers are recorded by the backend for auto-graded questions

## Adding Lessons

Create a Markdown file under `content/<course-id>/`.

Each lesson needs frontmatter like this:

```markdown
---
id: web-004
courseId: web-basics
title: Lesson title
description: Short description
phase: 1
order: 4
level: beginner
estimatedMinutes: 20
tags:
  - web
---
```

Quiz blocks are written at the end of the lesson:

~~~markdown
```quiz
id: web-004-q1
type: fill_blank
question: Question text
answer: Correct answer
explanation: Explanation text
```
~~~
