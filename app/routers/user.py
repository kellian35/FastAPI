from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_user

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user_route(user: UserCreate):
    created_user = await create_user(user)
    return created_user

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: str):
    user = await get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
