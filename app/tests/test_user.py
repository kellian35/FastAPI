import sys
import os
import pytest
import asyncio
from httpx import AsyncClient
from bson import ObjectId
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.schemas.user import UserCreate
from app.crud.user import create_user, get_user
from app.database.db import init_db, db


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    await init_db()
    yield
    await db["users"].delete_many({})
    logger.info("Database cleaned up after tests")

# Tests async avec AsyncClient pour faire des requêtes HTTP
@pytest.mark.asyncio
async def test_create_user_success():
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == user_data["full_name"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    logger.info(f"User created successfully with ID: {data['id']}")

@pytest.mark.asyncio
async def test_create_user_invalid_email():
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "email": "invalid-email"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/users/", json=user_data)
    assert response.status_code == 422
    logger.info("Invalid email correctly rejected")

@pytest.mark.asyncio
async def test_get_user_success():
    user_create = UserCreate(
        username="testuser2",
        full_name="Test User 2",
        email="test2@example.com"
    )
    created_user = await create_user(user_create)
    user_id = created_user["id"]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == user_create.full_name
    assert data["email"] == user_create.email
    assert data["id"] == user_id
    logger.info(f"User retrieved successfully: {user_id}")

@pytest.mark.asyncio
async def test_get_nonexistent_user():
    nonexistent_id = str(ObjectId())
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/v1/users/{nonexistent_id}")
    assert response.status_code == 404
    logger.info("Non-existent user correctly returned 404")

@pytest.mark.asyncio
async def test_get_user_invalid_id():
    invalid_id = "invalid-id-format"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/v1/users/{invalid_id}")
    assert response.status_code == 404
    logger.info("Invalid ID format correctly handled")
