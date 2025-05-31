from typing import Optional
from fastapi import FastAPI
from app.routers import user
from dotenv import load_dotenv
import os
from app.database import engine, Base

# .envファイルをロード
load_dotenv()

# 環境変数を取得
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# テーブルを作成
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])

# 簡易的なルート（動作確認用）
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the API!"
    }
