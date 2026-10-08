from config import SessionDep
from models import (
    Column,
    Board
)
from exceptions.http import (
    column_not_found
)
from sqlalchemy import select
import logging

db_logger = logging.getLogger('database')

async def validation_task(
    project_id: int,
    column_id: int,
    session: SessionDep,
) -> None: 

    db_logger.debug(
        "Validation task started: project_id = %s column_id = %s",
        project_id,
        column_id
    )

    stmt = (
        select(Column)
        .join(Board, Column.board_id == Board.id)
        .where(
            Column.id == column_id,
            Board.project_id == project_id,
        )   
    )

    column = await session.scalar(stmt)

    if column is None:

        db_logger.warning(
            "Column not found: project_id = %s column_id = %s",
            project_id,
            column_id
        )

        raise column_not_found()

    db_logger.debug("Validation task successfuly: project_id = %s column_id = %s",
        project_id,
        column_id
    )