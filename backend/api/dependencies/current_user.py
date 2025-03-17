from typing import Annotated

from fastapi import Depends

from api.api_v1.authentication.fastapi_users import current_active_user
from core.models import User

CurrentActiveUserDep = Annotated[User, Depends(current_active_user)]