from fastapi import APIRouter, HTTPException, Depends
from app.models.user import UserRegister, UserLogin
from app.utils.auth import create_access_token
from app.utils.hashing import verify_password, get_password_hash

router = APIRouter()

# Mock Database
users_db = {}

@router.post("/register")
def register_user(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    users_db[user.email] = {"password": hashed_password, "is_active": True}
    return {"message": "User registered successfully"}

@router.post("/login")
def login_user(user: UserLogin):
    db_user = users_db.get(user.email)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
