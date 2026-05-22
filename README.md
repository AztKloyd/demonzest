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

## First Setup On A New PC

Clone the repository:

```powershell
git clone https://github.com/AztKloyd/demonzest.git
cd demonzest
```

### 1. Prepare PostgreSQL

Option A: use Docker PostgreSQL:

Install Docker Desktop first, then run:

```powershell
docker compose up -d db
```

The Docker database uses:

```text
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=demonzest
HOST_PORT=5433
CONTAINER_PORT=5432
```

The host port is `5433` so it does not collide with a local PostgreSQL install that may already be using `5432`.

Stop the database:

```powershell
docker compose down
```

Reset the database volume:

```powershell
docker compose down -v
```

Option B: install PostgreSQL locally and create a database:

```sql
CREATE DATABASE demonzest;
```

The default local connection example is:

```text
postgresql+psycopg://postgres:password@localhost:5432/demonzest
```

Adjust the user, password, host, and database name for your machine.

### 2. Create Backend `.env`

From the project root:

```powershell
cd backend
copy .env.example .env
```

Edit `backend/.env`:

```text
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5433/demonzest
JWT_SECRET_KEY=change-this-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin-password123
ADMIN_NAME=Admin
CONTENT_DIR=../content
```

Use a private value for `JWT_SECRET_KEY` on your own machine.

### 3. Create Backend Virtual Environment

From `backend/`:

```powershell
py -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
```

If `py` is not available, use:

```powershell
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
```

### 4. Run Database Migration

From `backend/`:

```powershell
.\.venv\Scripts\alembic.exe upgrade head
```

### 5. Seed Admin User

From `backend/`:

```powershell
.\.venv\Scripts\python.exe scripts\seed_admin.py
```

### 6. Install Frontend Dependencies

Open another PowerShell from the project root:

```powershell
cd frontend
npm.cmd install
```

## Run Tests

Backend API smoke tests:

```powershell
cd backend
.\.venv\Scripts\pytest.exe
```

These tests use a temporary SQLite database and do not touch your local PostgreSQL data.

## Docker

Only PostgreSQL is Dockerized for now. Backend and frontend still run locally.

Install Docker Desktop before using these commands.

Start DB:

```powershell
docker compose up -d db
```

Check DB container:

```powershell
docker compose ps
```

Stop DB:

```powershell
docker compose down
```

Remove DB data and start fresh:

```powershell
docker compose down -v
docker compose up -d db
```

## Frontend API URL

Angular reads the API base URL from:

```text
frontend/src/environments/environment.ts
```

Default local value:

```ts
apiBaseUrl: 'http://localhost:8000/api'
```

For a deployed environment, update:

```text
frontend/src/environments/environment.prod.ts
```

## Start Backend

Open PowerShell:

```powershell
cd path\to\demonzest\backend
.\.venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000 --reload
```

Keep this terminal open.

## Start Frontend

Open another PowerShell:

```powershell
cd path\to\demonzest\frontend
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

## Common Problems

### Backend starts and immediately stops

Run it with reload:

```powershell
.\.venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000 --reload
```

The backend terminal should stay open. If it returns to the PowerShell prompt, the server is not running.

### Login says backend is not reachable

Check that FastAPI is running:

```text
http://127.0.0.1:8000/api/health
```

Expected response:

```json
{"status":"ok","service":"demonzest-api"}
```

### Database connection fails

Check `backend/.env`:

```text
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5433/demonzest
```

Confirm PostgreSQL is running and the database exists.

### Admin login fails

Run the seed script again:

```powershell
cd backend
.\.venv\Scripts\python.exe scripts\seed_admin.py
```

If the admin already exists with a different password, update the database record or create a different admin email in `.env`.

### PowerShell blocks npm.ps1

Use `npm.cmd` instead of `npm`:

```powershell
npm.cmd install
npm.cmd run start -- --host 127.0.0.1 --port 4200
```

## What Works Now

- Login with JWT stored in browser local storage
- Dashboard progress summary
- Roadmap and course detail pages
- Lesson reading page with formatted Markdown-like content
- Previous / next lesson navigation
- Lesson completion
- Quiz answer submission and grading result display
- Wrong answers are recorded by the backend for auto-graded questions
- Admin-only student account management
- Backend API smoke tests for login, roadmap, lesson, quiz submit, and admin user list

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
