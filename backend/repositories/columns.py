from models import (
    CreateColumn, 
    UpdateColumn,
    Column, 
)
from exceptions.http import column_not_found
from .common import execute_commit, requier_board, execute_scalars
from sqlalchemy import select, delete
from config import SessionDep
import logging

logger = logging.getLogger('database')

async def db_add_column(
    project_id: int,
    session: SessionDep,
    data: CreateColumn
): 

    logger.debug(
        "Create column started: project_id = %s",
        project_id
    )
    
    board = await requier_board(project_id, session)

    column = Column(
        title=data.title,
        board_id=board.id    
    )

    session.add(column)

    await execute_commit(session)
    await session.refresh(column)

    logger.debug(
        "Column created: project_id = %s column_id = %s",
        project_id,
        column.id
    )

    return column

async def db_get_columns(
    project_id: int,
    session: SessionDep
): 

    logger.debug(
        "Get columns started: project_id = %s",
        project_id
    )

    board = await requier_board(project_id, session)
    
    stmt = select(Column)\
    .where(Column.board_id == board.id)

    columns = await execute_scalars(session, stmt)

    logger.debug(
        "Columns retrieved: project_id = %s",
        project_id,
    )

    return columns.all()

async def db_get_column(
    project_id: int,
    column_id: int,
    session: SessionDep
): 

    logger.info(
        "Get column started: project_id = %s column_id = %s",
        project_id,
        column_id
    )
    
    board = await requier_board(project_id, session)

    stmt = select(Column)\
    .where(
        Column.board_id == board.id, 
        Column.id == column_id
    )

    column = await session.scalar(stmt)

    if column is None:

        logger.warning(
            "Column not found: project_id = %s column_id = %s",
            project_id,
            column_id
        )

        raise column_not_found()

    logger.info(
        "Column retrieve: project_id = %s column_id = %s",
        project_id,
        column_id
    )

    return column

async def db_update_column(
    project_id: int,
    column_id: int,
    session: SessionDep,
    data: UpdateColumn
): 

    logger.info(
        "Update column started: project_id = %s column_id = %s",
        project_id,
        column_id
    )
    
    await requier_board(project_id, session)

    stmt = select(Column)\
    .where(
        Column.id == column_id
    )

    column = await session.scalar(stmt)

    if column is None:

        logger.warning(
            "Column not found: project_id = %s column_id = %s",
            project_id,
            column_id
        )

        raise column_not_found()

    if data.title is not None:
        column.title = data.title

    await execute_commit(session)
    await session.refresh(column)

    logger.info(
        "Column updated: project_id = %s column_id = %s",
        project_id,
        column_id
    )   

    return column

async def db_delete_column(
    project_id: int,
    column_id: int,
    session: SessionDep
):

    logger.info(
        "Delete column: project_id = %s column_id = %s",
        project_id,
        column_id   
    )

    await requier_board(project_id, session)

    stmt = delete(Column)\
    .where(
        Column.id == column_id
    )

    result = await session.execute(stmt)
    await execute_commit(session)

    if result.rowcount == 0:

        logger.warning(
            "Column not found: project_id = %s column_id = %s",
            project_id,
            column_id
        )

        raise column_not_found()


    logger.info(
        "Column deleted: project_id = %s column_id = %s",
        project_id,
        column_id
    )