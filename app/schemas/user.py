from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str | None = None

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str | None = None
