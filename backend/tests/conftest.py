import sys
import os

import pytest_asyncio
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ["TESTING"] = "1"

from backend.core.config import settings
from main import main_app


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic upgrade heads")


CLEAN_TABLES = [
    "posts",
    "users",
]


@pytest_asyncio.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.db.url, future=True, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"TRUNCATE TABLE {table_for_cleaning} CASCADE;"))


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
    response = await client.post("/api/v1/auth/register", json=registration_data)
    # Если пользователь уже существует, можно обработать этот кейс
    assert response.status_code in (200, 201), response.text
    return registration_data
