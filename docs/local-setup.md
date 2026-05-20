# Local Setup

## Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `backend/.env` and set your local PostgreSQL connection string.
Also set the local development admin account values:

```env
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin-password123
ADMIN_NAME=Admin
```

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

## Seed First Admin User

After running migrations, create the first admin user:

```powershell
cd backend
.\.venv\Scripts\python.exe scripts\seed_admin.py
```

After that, `POST /api/users` requires an admin access token.

## Important

Do not commit `backend/.env`, `.venv`, or local database files.
