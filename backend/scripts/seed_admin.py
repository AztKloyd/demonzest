from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BACKEND_DIR))

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.enums import UserRole
from app.models.user import User


def main() -> None:
    if not settings.admin_email or not settings.admin_password:
        raise RuntimeError("ADMIN_EMAIL and ADMIN_PASSWORD must be set in .env")

    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.email == settings.admin_email).first()
        if existing_admin:
            print(f"Admin already exists: {existing_admin.email}")
            return

        admin = User(
            email=settings.admin_email,
            password_hash=hash_password(settings.admin_password),
            name=settings.admin_name,
            role=UserRole.ADMIN,
        )
        db.add(admin)
        db.commit()
        print(f"Admin created: {admin.email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
