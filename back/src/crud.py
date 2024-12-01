from fastapi import Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from back.src.database import get_db
from back.src.schemas import RecipeOptionDto
from back.src import models
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.functions import ST_Distance_Sphere, ST_GeomFromText

def build_prompt(dto: RecipeOptionDto) -> str:
    # options = request.value
    # store = options[1].value if len(options) > 1 and options[1].value else "Unknown Store"
    # max_amount = options[0].value if len(options) > 0 and options[0].value else 0
    # inserted_keyword = options[2].value if len(options) > 2 and options[2].value else "키워드 없음"
    store = dto.value[2]  # 편의점 이름
    max_amount = dto.value[0]  # 가격
    inserted_keyword = dto.value[1]  # 키워드

    # 여기에 키워드를 처리하는 부분이 필요할 수 있음 (예시에서는 생략)
    display_keyword = inserted_keyword  # 실제 맵핑 로직 추가 가능

    prompt = f"""
        편의점 {store}에서 {max_amount}원으로 {display_keyword}를 만족하는 맛있는 식사를 구성해주세요.

        다음 내용을 반드시 포함하여 한국어로 답변을 작성하세요:
        1. 각 제품의 이름, 가격, 특징을 목록으로 제시
        2. 총합 계산
        3. 추천 식사 구성을 작성
        사용자 요구 사항을 반영하여, 제품의 구성을 조정해야 합니다.

        내용 각각을 독립적인 문단으로 작성하세요.
    """

    return prompt

async def get_price_id(price_name: str, db: AsyncSession = Depends(get_db)):
    # Select statement using AsyncSession
    stmt = select(models.PriceRange).filter(models.PriceRange.price_name == price_name)
    result = await db.execute(stmt)
    price = result.scalars().first()  # Get the first result
    
    if not price:
        raise HTTPException(status_code=404, detail="Price range not found")
    
    return price.price_id

async def get_keyword_id(keyword_name: str, db: AsyncSession = Depends(get_db)):
    # Select statement using AsyncSession
    stmt = select(models.Keyword).filter(models.Keyword.keyword_name == keyword_name)
    result = await db.execute(stmt)
    keyword = result.scalars().first()  # Get the first result
    
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    
    return keyword.keyword_id

async def get_cstore_id(cstore_name: str, db: AsyncSession = Depends(get_db)):
    # Select statement using AsyncSession
    stmt = select(models.StoreType).filter(models.StoreType.cstore_name == cstore_name)
    result = await db.execute(stmt)
    storeType = result.scalars().first()  # Get the first result
    
    if not storeType:
        raise HTTPException(status_code=404, detail="Store Type not found")
    
    return storeType.cstore_id

async def get_nearby_stores(user_location: tuple, radius: int = 1000, db: AsyncSession = Depends(get_db)):
    # Convert user_location tuple to POINT geometry
    user_point = f"POINT({user_location[1]} {user_location[0]})"
    
    # Perform the query using execute (asynchronously)
    result = await db.execute(
        text("""
            SELECT store_id, store_name, address, ST_AsText(location) as location
            FROM store
            WHERE ST_Distance_Sphere(location, ST_GeomFromText(:user_point, 4326)) <= :radius
        """),
        {"user_point": user_point, "radius": radius}
    )
    
    # Fetch all results
    stores = result.fetchall()
    
    return stores