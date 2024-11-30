from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.schemas import RecipeOptionDto
from src import models
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

def get_price_id(db: Session, price_name: str):
    # 가격 정보에 해당하는 ID를 찾습니다.
    price = db.query(models.PriceRange).filter(models.PriceRange.price_name == price_name).first()
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    return price.price_id

def get_keyword_id(db: Session, keyword: str):
    # 키워드에 해당하는 ID를 찾습니다.
    keyword_obj = db.query(models.Keyword).filter(models.Keyword.keyword_name == keyword).first()
    if not keyword_obj:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return keyword_obj.keyword_id

def get_cstore_id(db: Session, cstore_name: str):
    # 편의점 종류에 해당하는 ID를 찾습니다.
    cstore = db.query(models.StoreType).filter(models.StoreType.cstore_name == cstore_name).first()
    if not cstore:
        raise HTTPException(status_code=404, detail="Store type not found")
    return cstore.cstore_id

def get_nearby_stores(db: Session, user_location: tuple, radius: int = 1000):
    user_point = ST_GeomFromText(f"POINT({user_location[0]} {user_location[1]})", srid=4326)
    return db.query(models.Store).filter(
        ST_Distance_Sphere(models.Store.location, user_point) <= radius
    ).all()