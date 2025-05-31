from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.models.users import User
from app.database import get_db
from app.utils.hashing import get_password_hash, verify_password
from app.utils.auth import create_access_token, decode_access_token
from fastapi.security import OAuth2PasswordBearer
from typing import Dict

router = APIRouter()

# 認証トークンの受け取り
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Pydanticモデル（リクエストデータのバリデーション）
class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    role: str

# ユーザーをメールアドレスで取得する関数
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# ユーザー登録
@router.post("/register", response_model=Dict[str, str])
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(email=user_data.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

# ユーザーログイン
@router.post("/login", response_model=Dict[str, str])
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# 認証済みユーザー情報取得
@router.get("/me", response_model=UserResponse)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return {"email": user.email, "role": user.role}

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
