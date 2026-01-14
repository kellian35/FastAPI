from app.models.user import User
from app.database.db import db
from bson import ObjectId
from bson.errors import InvalidId
import logging

logger = logging.getLogger(__name__)

async def create_user(user: User):
    logger.debug(f"Creating user in database: {user.email}")
    try:
        user_dict = user.dict()
        result = await db.users.insert_one(user_dict)
        created_user = await db.users.find_one({"_id": result.inserted_id})
        created_user["id"] = str(created_user["_id"])
        del created_user["_id"]
        logger.debug(f"User created in database: {created_user['id']}")
        return created_user
    except Exception as e:
        logger.error(f"Database error creating user: {str(e)}", exc_info=True)
        raise

async def get_user(user_id: str):
    logger.debug(f"Fetching user from database: {user_id}")
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
            logger.debug(f"User found in database: {user_id}")
        else:
            logger.debug(f"User not found in database: {user_id}")
        return user
    except InvalidId:
        logger.warning(f"Invalid user ID format: {user_id}")
        return None
    except Exception as e:
        logger.error(f"Database error fetching user: {str(e)}", exc_info=True)
        raise
