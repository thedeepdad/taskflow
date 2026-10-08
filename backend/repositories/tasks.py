from config import SessionDep
from models import (
    UpdateTask,
    CreateTask,
    User,
    Task, 
)
from exceptions.http import assignee_not_found
from .common import validation_task, execute_commit
from exceptions.http import task_not_found
from sqlalchemy import select, delete
import logging

db_logger = logging.getLogger('database')

async def db_add_task(
    project_id: int,
    column_id: int,
    session: SessionDep,
    data: CreateTask,
    user: User
): 

    db_logger.info(
        "Create task: project_id = %s column_id = %s user_id = %s",
        project_id,
        column_id,
        user.id
    )

    await validation_task(
        project_id,
        column_id,
        session
    )

    if data.assignee_id is not None:
        user = await session.get(User, data.assignee_id)

        db_logger.warning(
            "Task not found: project_id = %s column_id = %s user_id = %s",
            project_id,
            column_id,
            user.id
        )

        if user is None:
            raise assignee_not_found()

    task = Task(
        title=data.title,
        description=data.description,
        priority=data.priority,
        project_id=project_id,
        column_id=column_id,
        creator_id=user.id,
        due_date=data.due_date,
        assignee_id=data.assignee_id
    )

    session.add(task)

    await execute_commit(session)  
    await session.refresh(task)

    db_logger.info(
        "Task created: project_id = %s column_id = %s user_id = %s",
        project_id,
        column_id,
        user.id
    )

    return task

async def db_get_tasks(
    project_id: int,
    column_id: int,
    session: SessionDep
):

    db_logger.info(
        "Get tasks: project_id = %s column_id = %s",
        project_id,
        column_id
    )

    await validation_task(
        project_id,
        column_id,
        session
    )

    stmt = select(Task)\
    .where(Task.column_id == column_id)

    tasks = await session.scalars(stmt)

    db_logger.info(
        "Tasks retrieved: project_id = %s column_id = %s",
        project_id,
        column_id
    )

    return tasks.all()

async def db_get_task(
    project_id: int,
    column_id: int,
    task_id: int,
    session: SessionDep,
) -> Task: 

    db_logger.info(
        "Get task: project_id = %s column_id = %s task_id = %s",
        project_id,
        column_id,
        task_id
    )
    
    await validation_task(
        project_id,
        column_id,
        session
    )

    stmt = select(Task)\
    .where(Task.id == task_id)

    task = await session.scalar(stmt)

    if task is None:

        db_logger.warning(
            "Task not found: project_id = %s column_id = %s task_id = %s",
            project_id,
            column_id,
            task_id
        )

        raise task_not_found()

    db_logger.info(
        "Task retrieved: project_id = %s column_id = %s task_id = %s",
        project_id,
        column_id,
        task_id
    )

    return task

async def db_update_task(
    project_id: int,
    column_id: int,
    task_id: int,
    data: UpdateTask,
    session: SessionDep,            
): 

    db_logger.info(
        "Update task: project_id = %s column_id = %s task_id = %s",
        project_id,
        column_id,
        task_id
    )

    await validation_task(
        project_id,
        column_id,
        session
    )

    task = await session.get(Task, task_id)

    if task is None:

        db_logger.warning(
            "Task not found: project_id = %s column_id = %s task_id = %s",
            project_id,
            column_id,
            task_id
        )

        raise task_not_found()

    task.title = data.title
    task.description = data.description
    task.priority = data.priority
    task.due_date = task.due_date

    if data.assignee_id is not None:
        user = await session.get(User, data.assignee_id)

        if user is None:

            db_logger.warning(
                "Assignee not found: project_id = %s column_id = %s task_id = %s",
                project_id,
                column_id,
                task_id
            )

            raise assignee_not_found() 

    await execute_commit(session)
    await session.refresh(task)

    db_logger.info(
        "Task updated: project_id = %s column_id = %s task_id = %s",
        project_id,
        column_id,
        task_id
    )

    return task

async def db_delete_task(
    project_id: int,
    column_id: int,
    task_id: int,
    session: SessionDep        
): 

    db_logger.info(
        "Delete task: project_id = %s column_id = %s task_id = %s",
        project_id,
        column_id,
        task_id
    )
    
    await validation_task(
        project_id,
        column_id,
        session
    )    

    stmt = delete(Task)\
    .where(Task.id == task_id)

    result = await session.execute(stmt)
    await execute_commit(session)

    if result.rowcount == 0:

        db_logger.warning(
            "Task not found: project_id = %s column_id = %s task_id = %s",
            project_id,
            column_id,
            task_id
        )

        raise task_not_found()

    db_logger.info(
        "Task updated: project_id = %s column_id = %s task_id = %s",
        project_id,
        column_id,
        task_id
    )