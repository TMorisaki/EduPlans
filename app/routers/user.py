from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict
from app.schemas.user import UserRegister, UserLogin, UserResponse
from app.crud import user as crud
from app.database import get_db
from app.utils.hashing import verify_password
from app.utils.auth import create_access_token
from app.auth import user as auth_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=Dict[str, str])
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_user(db, user_data)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Dict[str, str])
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(auth_user.get_current_user)):
    return {"email": current_user.email, "role": current_user.role}
