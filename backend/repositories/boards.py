from models import (
    ProjectMember,
    UpdateBoard,
    CreateBoard, 
    Project, 
    Board, 
    User
)
from exceptions.http import (
    project_not_found, 
    requier_member, 
    board_already_exists,
    board_not_found
)
from config import SessionDep
from .common import execute_commit
from sqlalchemy import select, delete
import logging

logger = logging.getLogger('database')

async def db_add_board(
    project_id: int,
    data: CreateBoard,
    session: SessionDep,
    user: User
): 

    logger.info(
        "Create board started: project_id = %s user_id = %s",
        project_id,
        user.id
    )
    
    project = await session.get(Project, project_id)

    if project is None:

        logger.warning(
            "Project not found: project_id = %s user_id = %s",
            project_id,
            user.id
        )

        raise project_not_found()

    stmt = select(ProjectMember)\
    .where(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id
    )

    member = await session.scalar(stmt)

    if member is None:

        logger.warning(
            "User is not a member of this project: project_id = %s user_id = %s",
            project_id,
            user.id
        )

        raise requier_member()

    stmt = select(Board)\
    .where(Board.project_id == project_id)

    board = await session.scalar(stmt)

    if board is not None:

        logger.warning(
            "Board already exists: project_id = %s user_id = %s",
            project_id,
            user.id
        )

        raise board_already_exists()

    board = Board(
        name=data.name,
        project_id=project_id
    )

    session.add(board)

    await execute_commit(session)

    await session.refresh(board)

    logger.info(
        "Created board: project_id = %s user_id = %s",
        project_id,
        user.id
    )

    return board

async def db_get_board(
    project_id: int,
    session: SessionDep
): 

    logger.info(
        "Get board started: project_id = %s",
        project_id
    )
    
    stmt = select(Board)\
    .where(Board.project_id == project_id)

    board = await session.scalar(stmt)

    if board is None:

        logger.warning(
            "Board not found: project_id = %s",
            project_id
        )

        raise board_not_found()

    logger.info(
        "Board retrieved: project_id = %s",
        project_id
    )

    return board

async def db_update_board(
    project_id: int,
    session: SessionDep,
    data: UpdateBoard
): 

    logger.info(
        "Update board started: project_id = %s",
        project_id
    )
    
    stmt = select(Board)\
    .where(Board.project_id == project_id)

    board = await session.scalar(stmt)

    if board is None:

        logger.warning(
            "Board not found: project_id = %s",
            project_id
        )

        raise board_not_found()
    
    board.name = data.name

    await execute_commit(session)

    await session.refresh(board)

    logger.info(
        "Board updated: project_id = %s",
        project_id
    )

    return board

async def db_delete_board(
    project_id: int,
    session: SessionDep
): 

    logger.info(
        "Delete board started: project_id = %s",
        project_id
    )
    
    stmt = delete(Board)\
    .where(Board.project_id == project_id)

    result = await session.execute(stmt)
    await execute_commit(session)

    if result.rowcount == 0:

        logger.warning(
            "Board not found: project_id = %s",
            project_id
        )

        raise board_not_found()

    logger.info(
        "Board deleted: project_id = %s",
        project_id
    )