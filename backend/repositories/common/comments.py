from models import (
    Project, 
    Board, 
    Column, 
    Task
)
from config import SessionDep
from fastapi import HTTPException, status
from sqlalchemy import select
import logging

logger = logging.getLogger('database')

async def validation_comment(
    project_id: int,
    column_id: int,
    task_id: int,
    session: SessionDep,     
):

    logger.debug("Validation comment started: project_id = %s column_id = %s task_id = %s",
        project_id,
        column_id,
        task_id
    )
    
    project = await session.get(Project, project_id)

    if project is None:

        logger.warning(
            "Project not found: project_id = %s column_id = %s task_id = %s",
            project_id,
            column_id,
            task_id
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project not found'
        )

    stmt = select(Board)\
    .where(Board.project_id == project_id)

    board = await session.scalar(stmt)

    if board is None: 

        logger.warning(
            "Board not found: project_id = %s column_id = %s task_id = %s",
            project_id,
            column_id,
            task_id
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Board not found'
        )

    stmt = select(Column)\
    .where(
        Column.id == column_id,
        Column.board_id == board.id
    )

    column = await session.scalar(stmt)

    if column is None:

        logger.warning(
            "Column not found: project_id = %s column_id = %s task_id = %s",
            project_id,
            column_id,
            task_id
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Column not found'
        )

    stmt = select(Task)\
    .where(
        Task.id == task_id,
        Task.column_id == column_id
    )

    task = await session.scalar(stmt)

    if task is None:

        logger.warning(
            "Task not found: project_id = %s column_id = %s task_id = %s",
            project_id,
            column_id,
            task_id
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )

    logger.debug(
        "Validation comment successfuly: project_id = %s column_id = %s task_id = %s",
        project_id,
        column_id,
        task_id
    )