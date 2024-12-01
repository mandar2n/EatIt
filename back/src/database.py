##src.database.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import sys

# 프로젝트 디렉토리를 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# .env 파일에서 환경 변수 로드
load_dotenv()

# DATABASE_URL 환경 변수를 불러옴
DATABASE_URL = os.getenv("DATABASE_URL")

# Async engine 생성
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

# initialize database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# get_db 함수 추가
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            pass