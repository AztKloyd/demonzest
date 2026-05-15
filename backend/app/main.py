## FastAPIエントリーポイント

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
# CORSミドルウェアの設定
app.add_middleware( 
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,  # すべてのオリジンを許可
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

app.include_router(api_router, prefix=settings.api_prefix)