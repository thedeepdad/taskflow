from config import (
    log_execute,
    SessionDep,
    Prefix,
    Tags
)
from models import (
    UpdateTask,
    ResponseTask,
    CreateTask,
    User,
    Task
)
from fastapi import (
    status,
    APIRouter,
    Depends
)
from repositories import (
    db_delete_task,
    db_update_task,
    db_add_task,
    db_get_tasks,
    db_get_task
)
from dependencies import (
    requier_project_member,
    requier_project_manager
)
from typing import Annotated
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=Prefix.tasks,
    tags=[Tags.tasks]
)


@log_execute
@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseTask
)
async def add_tasks(
    project_id: int,
    column_id: int,
    session: SessionDep,
    data: CreateTask,
    current_user: Annotated[User, Depends(requier_project_member)]
) -> ResponseTask:

    task = await db_add_task(
        project_id,
        column_id,
        session,
        data,
        current_user
    )

    return task


@log_execute
@router.get(
    '',
    response_model=list[ResponseTask]
)
async def get_tasks(
    project_id: int,
    column_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_member)]
) -> list[ResponseTask]:

    tasks = await db_get_tasks(
        project_id,
        column_id,
        session,
    )

    return tasks


@log_execute
@router.get(
    '/{task_id}',
    response_model=ResponseTask
)
async def get_task(
    project_id: int,
    column_id: int,
    task_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_member)]
) -> Task:

    task = await db_get_task(
        project_id,
        column_id,
        task_id,
        session
    )

    return task


@log_execute
@router.patch(
    '/{task_id}',
    response_model=ResponseTask
)
async def change_task(
    project_id: int,
    column_id: int,
    task_id: int,
    data: UpdateTask,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_member)]
):

    task = await db_update_task(
        project_id,
        column_id,
        task_id,
        data,
        session
    )

    return task


@log_execute
@router.delete(
    '/{task_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    project_id: int,
    column_id: int,
    task_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_manager)]
):

    await db_delete_task(
        project_id,
        column_id,
        task_id,
        session
    )
