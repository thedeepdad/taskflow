from exceptions.http import (
    project_not_found, 
    board_not_found
)
from config import SessionDep
from models import Board, Project
from sqlalchemy import select
import logging

logger = logging.getLogger('database')


async def requier_board(
    project_id: int,
    session: SessionDep    
) -> Board: 

    project = await session.get(Project, project_id)

    if project is None:

        logger.warning(
            "Project not found: project_id = %s",
            project_id
        )

        raise project_not_found()

    stmt = select(Board)\
    .where(Board.project_id == project_id)

    board = await session.scalar(stmt)

    if board is None:

        logger.warning(
            "Board not found: project_id = %s",
            project_id
        )

        raise board_not_found()

    return board
    