from typing import Annotated

from fastapi import Depends

from core.utils.unit_of_work import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]