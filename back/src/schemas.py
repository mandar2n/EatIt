from pydantic import BaseModel
from typing import List

# User 위치 정보
class UserLocationDto(BaseModel):
    longitude: float
    latitude: float

# Store 리스트 조회 응답
class StoreListDto(BaseModel):
    store_id: int
    store_name: str
    address: str
    latitude: float
    longitude: float
    
# Recipe 리스트 조회 응답
class RecipeDto(BaseModel):
    recipe_name: str
    description: str
    price_id: int
    keyword_id: int
    cstore_id: int

# 각 옵션 값에 대한 모델
class OptionValueDto(BaseModel):
    display: str
    value: str  # 또는 해당하는 다른 타입, 예: int, float 등

# 레시피 옵션 정보 DTO
class OptionDto(BaseModel):
    display: str
    value: List[OptionValueDto]

# 레시피 생성에 필요한 입력
class RecipeOptionDto(BaseModel):
    value: List[OptionDto]
    recipe_name: str  # 레시피 이름

# AI로 생성된 레시피 응답
class AIGeneratedRecipeDto(BaseModel):
    recipe_result: str
