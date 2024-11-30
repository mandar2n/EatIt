from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config.settings import DATABASE_URL
import asyncio

# Async engine 생성
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# 비동기 세션 설정
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # commit할 때 객체를 만료시키지 않음
)

# Base 클래스
Base = declarative_base()

# DB 초기화 함수 (테이블 생성)
async def init_db():
    # 비동기적으로 메타데이터 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# DB 세션 함수
async def get_db():
    # 세션을 비동기적으로 가져오기
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            pass

# 이 코드에서 중요한 부분:
# 1. `future=True`: 비동기 작업을 위한 적절한 동작을 보장합니다.
# 2. `SessionLocal`을 비동기 세션으로 설정하여, 모든 데이터베이스 작업을 비동기적으로 처리합니다.
