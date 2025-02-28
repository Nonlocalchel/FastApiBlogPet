import sys
import os

import asyncpg
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.config import settings
import pytest
from httpx import AsyncClient, ASGITransport

from main import main_app

# def pytest_configure(config):
#     config.option.asyncio_default_fixture_loop_scope = "function"
#
# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
#
# test_engine = create_async_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False}
# )
# TestingSessionLocal = async_sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=test_engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )
#
# @pytest_asyncio.fixture(scope="session")
# async def db_engine():
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#     yield test_engine
#
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#
# @pytest.fixture(scope="function")
# def db_session(db_engine):
#     session = TestingSessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()
#
# @pytest.fixture(autouse=True)
# def override_get_db(db_session):
#     """
#     Переопределяем зависимость get_db, чтобы она использовала сессию из тестовой базы.
#     """
#     def _get_db():
#         try:
#             yield db_session
#         finally:
#             pass
#
#     main_app.dependency_overrides[db_helper.session_factory] = _get_db
#     yield
#     main_app.dependency_overrides.clear()
# CLEAN_TABLES = [
#     "users",
# ]

# @pytest.fixture(scope="session", autouse=True)
# async def run_migrations():
#     os.system("alembic init migrations")
#     os.system('alembic revision --autogenerate -m "test running migrations"')
#     os.system("alembic upgrade heads")


# @pytest.fixture(scope="session")
# async def async_session_test():
#     engine = create_async_engine(
#         settings.db.url,
#         connect_args={"check_same_thread": False}
#     )
#     async_session = async_sessionmaker(
#         autocommit=False,
#         autoflush=False,
#         bind=engine,
#         class_=AsyncSession,
#         expire_on_commit=False
#     )
#     yield async_session

#
# @pytest.fixture(scope="function", autouse=True)
# async def clean_tables(async_session_test):
#     """Clean data in all tables before running test function"""
#     async with async_session_test() as session:
#         async with session.begin():
#             for table_for_cleaning in CLEAN_TABLES:
#                 await session.execute(f"""TRUNCATE TABLE {table_for_cleaning};""")


# async def _get_test_db():
#     try:
#         test_engine = create_async_engine(
#             settings.db.url,
#             connect_args={"check_same_thread": False}
#         )
#         test_async_session = async_sessionmaker(
#             autocommit=False,
#             autoflush=False,
#             bind=test_engine,
#             class_=AsyncSession,
#             expire_on_commit=False
#         )
#         yield test_async_session()
#     finally:
#         pass


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
            transport=ASGITransport(app=main_app),
            base_url="http://test",
    ) as ac:
        yield ac


# @pytest.fixture(scope="session")
# async def asyncpg_pool():
#     pool = await asyncpg.create_pool(
#         "".join(settings.TEST_DATABASE_URL.split("+asyncpg"))
#     )
#     yield pool
#     pool.close()


