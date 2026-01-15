from app.models.user import User
from app.database.db import db
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

async def create_user(user: User):
    logger.debug(f"Creating user in database: {user.email}")
    try:
        user_dict = user.dict()
        # Ajout des champs pour soft delete
        user_dict.update({
            "is_active": True,
            "deleted_at": None
        })
        result = await db.users.insert_one(user_dict)
        created_user = await db.users.find_one({"_id": result.inserted_id})
        if created_user:
            created_user["id"] = str(created_user["_id"])
            del created_user["_id"]
            logger.debug(f"User created in database: {created_user['id']}")
        return created_user
    except Exception as e:
        logger.error(f"Database error creating user: {str(e)}", exc_info=True)
        raise

async def get_user(user_id: str, active_only: bool = True):
    logger.debug(f"Fetching user from database: {user_id}")
    try:
        query = {"_id": ObjectId(user_id)}
        query["is_active"] = True
        user = await db.users.find_one(query)
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
            logger.debug(f"User found in database: {user_id}")
        else:
            logger.debug(f"User not found or inactive in database: {user_id}")
        return user
    except InvalidId:
        logger.warning(f"Invalid user ID format: {user_id}")
        return None
    except Exception as e:
        logger.error(f"Database error fetching user: {str(e)}", exc_info=True)
        raise

async def get_users(active_only: bool = True):
    logger.debug(f"Fetching all users from database")
    try:
        query = {}
        query["is_active"] = True
        users = await db.users.find(query).to_list(length=None)
        for user in users:
            user["id"] = str(user["_id"])
            del user["_id"]
        logger.debug(f"Fetched {len(users)} users from database")
        return users
    except Exception as e:
        logger.error(f"Database error fetching users: {str(e)}", exc_info=True)
        raise

async def get_all_users_deactivate():
    logger.debug(f"Fetching all users from database (including inactive)")
    try:
        users = await db.users.find().to_list(length=None)
        for user in users:
            user["id"] = str(user["_id"])
            del user["_id"]
        logger.debug(f"Fetched {len(users)} users from database")
        return users
    except Exception as e:
        logger.error(f"Database error fetching users: {str(e)}", exc_info=True)
        raise

async def deactivate_user(user_id: str):
    logger.debug(f"Deactivating user: {user_id}")
    try:
        result = await db.users.update_one(
            {"_id": ObjectId(user_id), "is_active": True},
            {
                "$set": {
                    "is_active": False,
                    "deleted_at": datetime.utcnow()
                }
            }
        )
        if result.modified_count == 0:
            logger.warning(f"User not found or already inactive: {user_id}")
            return False
        logger.info(f"User deactivated successfully: {user_id}")
        return True
    except InvalidId:
        logger.warning(f"Invalid user ID format: {user_id}")
        return False
    except Exception as e:
        logger.error(f"Database error deactivating user: {str(e)}", exc_info=True)
        raise
