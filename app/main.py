from fastapi import FastAPI
from app.routers import user
from dotenv import load_dotenv
import os

# .envファイルをロード
load_dotenv()

# 環境変数を取得
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# アプリケーションインスタンスの作成
app = FastAPI()

# ルーターの登録
app.include_router(user.router, prefix="/users", tags=["users"])

# 簡易的なルート（動作確認用）
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the API!",
        "SECRET_KEY": SECRET_KEY,
        "DATABASE_URL": DATABASE_URL,
    }
