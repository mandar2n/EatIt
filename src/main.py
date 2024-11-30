from fastapi import FastAPI
from src.database import init_db
from src.database import engine, SessionLocal
from src.routers import recipes

from src.models import Base

app = FastAPI()
app.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])

# @app.on_event("startup")
# async def startup_event():
#     # DB 테이블 생성
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def read_root():
    return {"message": "Welcome"}