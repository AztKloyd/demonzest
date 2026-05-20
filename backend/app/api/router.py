from fastapi import APIRouter

from app.api.routes import auth, db_health, health, lessons, me, quiz, review, users


api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(db_health.router)
api_router.include_router(users.router)
api_router.include_router(auth.router)
api_router.include_router(me.router)
api_router.include_router(lessons.router)
api_router.include_router(quiz.router)
api_router.include_router(review.router)
