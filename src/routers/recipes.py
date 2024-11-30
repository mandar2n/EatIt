import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src import schemas, crud, models
from src.database import get_db
import openai  # OpenAI API 연결
from dotenv import load_dotenv
from src.schemas import OptionValueDto, OptionDto
from typing import List

# .env 파일에서 환경 변수 로드
load_dotenv()

router = APIRouter()

# OpenAI API 연결 초기화
openai.api_key = os.getenv("OPENAI_API_KEY")  

# 레시피 옵션 정보 반환 (가격대, 편의점 종류, 키워드)
@router.get("/options", response_model=List[OptionDto])
def get_recipe_options():
    options = [
        OptionDto(
            display="최대 금액 선택",
            value=[
                OptionValueDto(display="5000원", value="5000"),
                OptionValueDto(display="8000원", value="8000"),
                OptionValueDto(display="10000원", value="10000")
            ]
        ),
        OptionDto(
            display="편의점 선택",
            value=[
                OptionValueDto(display="GS25", value="GS25"),
                OptionValueDto(display="CU", value="CU"),
                OptionValueDto(display="세븐일레븐", value="7ELEVEN")
            ]
        ),
        OptionDto(
            display="키워드",
            value=[
                OptionValueDto(display="상큼한 비타민", value="vitamin"),
                OptionValueDto(display="에너지 넘치는 영양소", value="nutritious"),
                OptionValueDto(display="건강한 저당", value="healthy_low_sugar"),
                OptionValueDto(display="아삭한 식이섬유", value="dietary_fiber"),
                OptionValueDto(display="균형 잡힌 식단", value="balanced_diet"),
                OptionValueDto(display="가벼운 저칼로리", value="low_calorie")
            ]
        )
    ]
    return options

# AI 레시피 생성 및 DB 저장
@router.post("/generate", response_model=schemas.AIGeneratedRecipeDto)
async def generate_recipe(dto: schemas.RecipeOptionDto, db: Session = Depends(get_db)):
    
    # 프롬프트 생성
    prompt = crud.build_prompt(dto)
    
    # OpenAI API에 요청 (ChatGPT로 레시피 생성)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},  # Pass the prompt here
        ],
        max_tokens=500
    )

    # AI가 생성한 레시피 결과
    recipe_result = response['choices'][0]['message']['content'].strip()
    
    price_name = dto.value[0].value[0].display  # Extract the price value from the DTO
    price_id = await crud.get_price_id(price_name=price_name, db=db)  # Call the function with the correct value

    keyword_name = dto.value[1].value[0].display  # Extract the price value from the DTO
    keyword_id = await crud.get_keyword_id(keyword_name=keyword_name, db=db)  # Call the function with the correct value
    
    cstore_name = dto.value[2].value[0].display   # Extract the price value from the DTO
    cstore_id = await crud.get_cstore_id(cstore_name=cstore_name, db=db)  # Call the function with the correct value
    
   
    print(f"Extracted price_name: {price_name}")  # Debugging
    print(f"Extracted keyword_name: {keyword_name}")  # Debugging
    print(f"Extracted cstore_name: {cstore_name}")  # Debugging
    
    # DB에 저장 (Recipe 모델에 맞춰 저장)
    new_recipe = models.Recipe(
        recipe_name=dto.recipe_name,  # 사용자로부터 입력받은 레시피 이름
        description=recipe_result,  # AI가 생성한 레시피
        price_id=price_id,  # 조회한 가격 ID
        keyword_id=keyword_id,  # 조회한 키워드 ID
        cstore_id=cstore_id   # 조회한 편의점 ID
    )
    
    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)
    
    return {"recipe_result": new_recipe.description}
