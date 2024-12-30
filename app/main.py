from fastapi import FastAPI
from app.routers import user

app = FastAPI()

# ルーターの登録
app.include_router(user.router, prefix="/users", tags=["users"])
