from typing import Annotated

from fastapi import Depends , Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page : Annotated[int | None, Query(None, description="Номер страницы",ge=1,lt=30)]    
    per_page: Annotated[int | None, Query(None, description="Количество объектов на странице", ge=1,lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]