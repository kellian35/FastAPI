from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_user, get_users
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    response_description="User created successfully"
)
async def create_user_route(user: UserCreate):
    logger.info(f"Creating new user: {user.email}")
    try:
        created_user = await create_user(user)
        logger.info(f"User created successfully: {created_user['id']}")
        return created_user
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    response_description="User details"
)
async def read_user(user_id: str):
    logger.info(f"Fetching user with ID: {user_id}")
    try:
        user = await get_user(user_id)
        if user is None:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        logger.info(f"User fetched successfully: {user_id}")
        return user
    except Exception as e:
        logger.error(f"Error fetching user: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get(
    "/",
    response_model=list[UserResponse],
    response_description="List of all users")
async def read_users():
    logger.info("Fetching all users")
    try:
        users = await get_users()
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )