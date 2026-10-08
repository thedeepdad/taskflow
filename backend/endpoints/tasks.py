from config import (
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

    logger.info(
        "Create task started: project_id = %s column_id = %s user_id = %s",
        project_id,
        column_id,
        current_user.id 
    )
     
    task = await db_add_task(
        project_id,
        column_id,
        session,
        data,
        current_user
    )

    logger.info(
        "Task created: project_id = %s column_id = %s task_id = %s user_id = %s",
        project_id,
        column_id,
        task.id,
        current_user.id
    )

    return task

@router.get(
    '',
    response_model=list[ResponseTask]
)
async def get_tasks(
    project_id: int,
    column_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_member)]
) -> list[ResponseTask]:

    logger.info(
        "Get tasks started: project_id = %s column_id = %s user-id = %s",
        project_id,
        column_id,
        current_user.id
    )
     
    tasks = await db_get_tasks(
        project_id,
        column_id,
        session,
    )

    logger.info(
        "Tasks retrieved: project_id = %s column_id = %s count = %s user_id = %s",
        project_id,
        column_id,
        len(tasks),
        current_user.id
    )

    return tasks

@router.get(
    '/{task_id}',
    response_model=ResponseTask
)
async def get_task(
    project_id: int,
    column_id: int,
    task_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_member)]
) -> Task:

    logger.info(
        "Get task started: project_id = %s column_id = %s task_id = %s user_id = %s",
        project_id,
        column_id,
        task_id,
        current_user.id
    )
     
    task = await db_get_task(
        project_id,
        column_id,
        task_id,
        session
    )

    logger.info(
        "Task retrieved: project_id = %s column_id = %s task_id = %s user_id = %s",
        project_id,
        column_id,
        task_id,
        current_user.id
    )

    return task

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
    current_user: Annotated[User, Depends(requier_project_member)]
): 

    logger.info(
        "Change task started: project_id = %s column_id = %s task_id = %s user_id = %s",
        project_id,
        column_id,
        task_id,
        current_user.id
    )
    
    task = await db_update_task(
        project_id,
        column_id,
        task_id,
        data,
        session
    )

    logger.info(
        "Task changed: project_id = %s column_id = %s task_id = %s user_id = %s",
        project_id,
        column_id,
        task_id,
        current_user.id
    )

    return task

@router.delete(
    '/{task_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    project_id: int,
    column_id: int,
    task_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_manager)]
): 

    logger.info(
        "Delete task started: project_id = %s column_id = %s task_id = %s user_id = %s",
        project_id,
        column_id,
        task_id,
        current_user.id
    )
    
    await db_delete_task(
        project_id,
        column_id,
        task_id,
        session
    )

    logger.info(
        "Delete task: project_id = %s column_id = %s task_id = %s user_id = %s",
        project_id,
        column_id,
        task_id,
        session
    )