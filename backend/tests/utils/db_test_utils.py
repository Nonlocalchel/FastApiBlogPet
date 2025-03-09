import sys
import os

from sqlalchemy import text

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.utils import db_helper


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