from datetime import datetime, timedelta
from typing import Optional
import jwt  # PyJWT を使用
import os
from dotenv import load_dotenv

# .env ファイルをロード
load_dotenv()

# 環境変数からシークレットキーを取得
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")  # デフォルト値を指定
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 45))  # .env から取得、デフォルト 45 分

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT アクセストークンを作成"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    if isinstance(encoded_jwt, bytes):  # バージョンによっては bytes 型で返るため str に変換
        encoded_jwt = encoded_jwt.decode("utf-8")

    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """JWT アクセストークンをデコード"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
