# Local Setup

## Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `backend/.env` and set your local PostgreSQL connection string.

Run the API server:

```powershell
.\.venv\Scripts\uvicorn app.main:app --reload
```

Health check:

```txt
http://localhost:8000/api/health
```

Database health check:

```txt
http://localhost:8000/api/db-health
```

## Database Migration

```powershell
cd backend
.\.venv\Scripts\alembic upgrade head
```

## Important

Do not commit `backend/.env`, `.venv`, or local database files.
