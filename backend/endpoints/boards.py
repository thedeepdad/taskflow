from config import (
    log_execute,
    SessionDep,
    Prefix,
    Tags,
)
from models import (
    ResponseBoard,
    CreateBoard,
    UpdateBoard,
    User
)
from fastapi import (
    APIRouter,
    status,
    Depends
)
from repositories import (
    db_delete_board,
    db_update_board,
    db_get_board,
    db_add_board,
)
from dependencies import (
    requier_project_manager,
    requier_project_member
)
from typing import Annotated
import logging


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=Prefix.boards,
    tags=[Tags.boards]
)


@log_execute
@router.post(
    '',
    response_model=ResponseBoard,
    status_code=status.HTTP_201_CREATED
)
async def add_board(
    project_id: int,
    data: CreateBoard,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_manager)]
):

    board = await db_add_board(
        project_id,
        data,
        session,
        current_user
    )

    return board


@log_execute
@router.get(
    '',
    response_model=ResponseBoard
)
async def get_board(
    project_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_member)]
):

    board = await db_get_board(
        project_id,
        session
    )

    return board


@log_execute
@router.patch(
    '',
    response_model=ResponseBoard
)
async def update_board(
    project_id: int,
    session: SessionDep,
    data: UpdateBoard,
    _: Annotated[User, Depends(requier_project_manager)]
):

    board = await db_update_board(
        project_id,
        session,
        data
    )

    return board


@log_execute
@router.delete(
    '',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_board(
    project_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_manager)]
):

    await db_delete_board(
        project_id,
        session
    )
