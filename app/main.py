from fastapi import FastAPI
from app.database.db import init_db
from app.routers import user

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await init_db()

app.include_router(user.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Hello World"}
