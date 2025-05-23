import sys
import os

import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ["TESTING"] = "1"

from backend.core.schemas.posts import PostCreate
from backend.api.dependencies.services import posts_service
from backend.tests.utils.db_test_utils import run_migrations, remove_migrations
from backend.tests.utils.user_tests_utils import register_user, login_user

from main import main_app


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    loop.run_until_complete(run_migrations())
    yield loop
    loop.run_until_complete(remove_migrations()) #если ошибка миграций то заменить на truncate_tables
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(
            transport=ASGITransport(app=main_app),
            base_url="http://test",
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="session", autouse=True)
async def auth_header(client: AsyncClient):
    login = "test@example.com"
    password = "password"
    register_response = await register_user(client, (login, password))
    try:
        assert register_response.status_code in (200, 201), register_response.text
    except AssertionError:
        print('User is exist')

    login_response = await login_user(client, (login, password))
    assert login_response.status_code == 200, login_response.text
    token = login_response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture(scope="session", autouse=True)
async def last_post(client: AsyncClient, auth_header: dict):
    posts_service_obj = posts_service()
    last_post_id = ''
    posts_data = [
        {"title": "first", "body": "some text"}, {"title": "second", "body": "some text"},
        {"title": "third", "body": "some text"}, {"title": "fourth", "body": "some text"},
        {"title": "fifth", "body": "some text"}, {"title": "sixth", "body": "some text"},
    ]
    for post_data in posts_data:
        post = await posts_service_obj.add_post(PostCreate(**post_data))
        post_id = post.id
        assert type(post_id) == int
        last_post_id = post.id

    return int(last_post_id)
