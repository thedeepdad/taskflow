from config import (
    log_execute,
    SessionDep,
    Prefix,
    Tags,
)

from models import (
    ResponseComment,
    CreateComment,
    UpdateComment,
    User,
)

from fastapi import (
    APIRouter,
    status,
    Depends
)
from repositories import (
    db_delete_comment,
    db_update_comment,
    db_add_comment,
    db_get_comments,
    db_get_comment
)
from dependencies import (
    requier_project_member,
    requier_comment_owner_or_manager
)
from typing import Annotated
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=Prefix.comments,
    tags=[Tags.comments]
)


@log_execute
@router.post(
    '',
    response_model=ResponseComment,
    status_code=status.HTTP_201_CREATED
)
async def add_comment(
    project_id: int,
    column_id: int,
    task_id: int,
    data: CreateComment,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_member)]
):

    comment = await db_add_comment(
        project_id,
        column_id,
        task_id,
        data,
        session,
        current_user
    )

    return comment


@log_execute
@router.get(
    '',
    response_model=list[ResponseComment]
)
async def get_comments(
    project_id: int,
    column_id: int,
    task_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_member)]
):

    comments = await db_get_comments(
        project_id,
        column_id,
        task_id,
        session,
        current_user
    )

    return comments


@log_execute
@router.get(
    '/{comment_id}',
    response_model=ResponseComment
)
async def get_comment(
    project_id: int,
    column_id: int,
    task_id: int,
    comment_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_member)]
):

    comment = await db_get_comment(
        project_id,
        column_id,
        task_id,
        comment_id,
        session,
    )

    return comment


@log_execute
@router.patch(
    '/{comment_id}',
    response_model=ResponseComment
)
async def update_comment(
    project_id: int,
    column_id: int,
    task_id: int,
    comment_id: int,
    data: UpdateComment,
    session: SessionDep,
    _: Annotated[User, Depends(requier_comment_owner_or_manager)]
):

    comment = await db_update_comment(
        project_id,
        column_id,
        task_id,
        comment_id,
        data,
        session
    )

    return comment


@log_execute
@router.delete(
    '/{comment_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
    project_id: int,
    column_id: int,
    task_id: int,
    comment_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_comment_owner_or_manager)]
):

    await db_delete_comment(
        project_id,
        column_id,
        task_id,
        comment_id,
        session
    )
