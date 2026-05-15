##APIルーターを一つにまとめるためのファイル

from fastapi import APIRouter
from app.api.routes import health
from app.api.routes import db_health    

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(db_health.router)