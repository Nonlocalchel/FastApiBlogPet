import os

from sqlalchemy import text

from backend.core.utils import db_helper


async def run_migrations():
    os.system("alembic upgrade heads")


async def remove_migrations():
    os.system("alembic downgrade base")


CLEAN_TABLES = [
    "posts",
    "users",
]


async def truncate_tables():
    async with db_helper.session_factory() as session:
        async with session.begin():
            for table in CLEAN_TABLES:
                await session.execute(text(f"TRUNCATE TABLE {table} CASCADE;"))
