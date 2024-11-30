from fastapi import FastAPI
from src.database import init_db
from src.database import engine, SessionLocal

from src.models import Base

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # DB 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def read_root():
    return {"message": "DB Connection Successful"}