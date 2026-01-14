from app.models.user import User
from app.database.db import db
from bson import ObjectId

async def create_user(user: User):
    user_dict = user.dict()
    result = await db.users.insert_one(user_dict)
    created_user = await db.users.find_one({"_id": result.inserted_id})
    created_user["id"] = str(created_user["_id"])
    del created_user["_id"]
    return created_user

async def get_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"]
    return user
