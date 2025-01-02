from datetime import timedelta, datetime
from typing import Optional
import jwt
import os
from dotenv import load_dotenv

# .env ファイルをロード
load_dotenv()

# 環境変数からシークレットキーを取得
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")  # デフォルト値を指定
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=45))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
