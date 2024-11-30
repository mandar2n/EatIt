from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from src import crud, models  # Adjust import based on your project structure
from src.database import get_db
from src.schemas import StoreListDto, UserLocationDto


router = APIRouter()

@router.post("/nearby_stores", response_model=List[StoreListDto])
async def get_nearby_stores_api(user_location: UserLocationDto, db: Session = Depends(get_db)):
    # Get user location from the DTO
    user_location_tuple = (user_location.longitude, user_location.latitude)
    
    # Get nearby stores using the get_nearby_stores function
    stores = await crud.get_nearby_stores(user_location_tuple, radius=1000, db=db)  # 1km radius
    
    # Map the stores to the response DTO format
    store_list = [
        StoreListDto(
            store_id=store.store_id,
            store_name=store.store_name,
            address=store.address,
            location = store.location[6:-1],  # Remove 'POINT(' and ')'
            latitude=float(store.location[6:-1].split(" ")[1]),  # Extract latitude
            longitude=float(store.location[6:-1].split(" ")[0])  # Extract longitude
        )
        for store in stores
    ]
    
    return store_list