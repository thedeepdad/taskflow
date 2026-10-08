from config import (
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

    logger.info("Create board: project_id = %s user_id = %s",
        project_id,
        current_user.id
    )
    
    board = await db_add_board(
        project_id,
        data,
        session,
        current_user
    )

    logger.info("Board created: project_id = %s board_id = %s user_id = %s",
        project_id,
        board.id,
        current_user.id
    )

    return board

@router.get(
    '',
    response_model=ResponseBoard
)
async def get_board(
    project_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_member)]
): 
    logger.info("Get board: project_id = %s user_id = %s",
        project_id,
        current_user.id
    )
    
    board = await db_get_board(
        project_id,
        session
    )

    logger.info("Board retrieved: project_id = %s board_id = %s user_id = %s",
        project_id,
        board.id,
        current_user.id
    )

    return board

@router.patch(
    '',
    response_model=ResponseBoard
)
async def update_board(
    project_id: int,
    session: SessionDep,
    data: UpdateBoard,
    current_user: Annotated[User, Depends(requier_project_manager)]
): 

    logger.info("Update board: project_id = %s user_id = %s",
        project_id,
        current_user.id
    )
    
    board = await db_update_board(
        project_id,
        session,
        data
    )

    logger.info("Board updated: project_id = %s board_id = %s user_id = %s",
        project_id,
        board.id,
        current_user.id
    )

    return board

@router.delete(
    '',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_board(
    project_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_manager)]
): 

    logger.info("Delete board: proejct_id = %s user_id = %s",
        project_id,
        current_user.id
    )
    
    await db_delete_board(
        project_id,
        session
    )

    logger.info("Board deleted: project_id = %s user_id = %s",
        project_id,
        current_user.id
    )