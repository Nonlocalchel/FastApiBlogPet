from core.models import (
    db_helper,
    User
)


async def get_users_db():
    async with db_helper.session_factory() as session:
        yield User.get_db(session=session)
