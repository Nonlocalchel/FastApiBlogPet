import sys
import os

import pytest_asyncio
import asyncio

from sqlalchemy import text
from httpx import AsyncClient, ASGITransport

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ["TESTING"] = "1"

from backend.core.utils import db_helper
from main import main_app


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    loop.run_until_complete(run_migrations())
    yield loop
    loop.run_until_complete(truncate_tables())
    loop.close()


# @pytest_asyncio.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic upgrade heads")


CLEAN_TABLES = [
    "posts",
    "users",
]


async def truncate_tables():
    async with db_helper.session_factory() as session:
        async with session.begin():
            for table in CLEAN_TABLES:
                await session.execute(text(f"TRUNCATE TABLE {table} CASCADE;"))


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(
            transport=ASGITransport(app=main_app),
            base_url="http://test",
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_user(client: AsyncClient):
    registration_data = {
        "email": "test@example.com",
        "password": "password"
    }
    try:
        response = await client.post("/api/v1/auth/register", json=registration_data)
        # Если пользователь уже существует, можно обработать этот кейс
        assert response.status_code in (200, 201), response.text
    except AssertionError:
        print('User is exist(past tests execute error, past data didn\'t truncate)')
    finally:
        return registration_data


@pytest_asyncio.fixture(scope="session", autouse=True)
async def auth_token(client: AsyncClient, create_test_user):
    login_data = {
        "username": create_test_user["email"],
        "password": create_test_user["password"],
    }
    response = await client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200, response.text
    token = response.json().get("access_token")
    return token


@pytest_asyncio.fixture(scope="session", autouse=True)
async def test_create_posts(client: AsyncClient, auth_token: str):
    last_post_id = ''
    posts_data = [
        {"title": "first", "body": "some text"},
        {"title": "second", "body": "some text"},
        {"title": "third", "body": "some text"},
        {"title": "fourth", "body": "some text"},
        {"title": "fifth", "body": "some text"},
        {"title": "sixth", "body": "some text"},
    ]
    headers = {"Authorization": f"Bearer {auth_token}"}
    for post_data in posts_data:
        response = await client.post("/api/v1/posts/", json=post_data, headers=headers)
        assert response.status_code == 201
        last_post_id = response.json()['id']

    return last_post_id