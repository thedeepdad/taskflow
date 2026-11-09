from config import (
    Prefix,
    Tags,
    SessionDep
)
from models import (
    UpdateColumn,
    ResponseColumn,
    CreateColumn,
    User,
)
from fastapi import (
    APIRouter,
    Depends,
    status
)
from repositories import (
    db_delete_column,
    db_update_column,
    db_get_columns,
    db_add_column,
    db_get_column
)
from dependencies import (
    requier_project_manager,
    requier_project_member
)
from typing import Annotated
from config import log_execute
import logging


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=Prefix.columns,
    tags=[Tags.columns]
)


@log_execute
@router.post(
    '',
    response_model=ResponseColumn,
    status_code=status.HTTP_201_CREATED
)
async def add_column(
    project_id: int,
    data: CreateColumn,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_manager)]
):
    column = await db_add_column(
        project_id,
        session,
        data
    )

    return column


@log_execute
@router.get(
    '',
    response_model=list[ResponseColumn]
)
async def get_columns(
    project_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_member)]
):

    columns = await db_get_columns(
        project_id,
        session
    )

    return columns


@log_execute
@router.get(
    '/{column_id}',
    response_model=ResponseColumn
)
async def get_column(
    project_id: int,
    column_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_member)]
):

    column = await db_get_column(
        project_id,
        column_id,
        session
    )

    return column


@log_execute
@router.patch(
    '/{column_id}',
    response_model=ResponseColumn
)
async def update_column(
    project_id: int,
    column_id: int,
    session: SessionDep,
    data: UpdateColumn,
    _: Annotated[User, Depends(requier_project_manager)]
):

    column = await db_update_column(
        project_id,
        column_id,
        session,
        data
    )

    return column


@log_execute
@router.delete(
    '/{column_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_column(
    project_id: int,
    column_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_manager)]
):

    await db_delete_column(
        project_id,
        column_id,
        session
    )
