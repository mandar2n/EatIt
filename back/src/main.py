from fastapi import FastAPI
from back.src.database import init_db
from back.src.database import engine, SessionLocal
from back.src.routers import recipes, location
from fastapi.middleware.cors import CORSMiddleware

from back.src.models import Base

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],  # 프론트엔드 URL 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
app.include_router(location.router, prefix="/location", tags=["Location"])

# @app.on_event("startup")
# async def startup_event():
#     # DB 테이블 생성
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# FastAPI 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/")
async def read_root():
    return {"message": "Welcome"}