from core.models import User
from core.utils.db_session import session_factory


async def get_users_db():
    async with session_factory() as session:
        yield User.get_db(session=session)
