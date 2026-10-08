from config import (
    Prefix, 
    Tags, 
    SessionDep
)
from models import (
    UpdateColumn,
    ResponseColumn,
    CreateColumn, 
    User, 
)
from fastapi import (
    APIRouter, 
    Depends,
    status
)
from repositories import (
    db_delete_column,
    db_update_column,
    db_get_columns,
    db_add_column, 
    db_get_column
)
from dependencies import (
    requier_project_manager, 
    requier_project_member
)
from typing import Annotated
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=Prefix.columns, 
    tags=[Tags.columns]
)

@router.post(
    '',
    response_model=ResponseColumn,
    status_code=status.HTTP_201_CREATED
)
async def add_column(
    project_id: int,
    data: CreateColumn,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_manager)]
): 
    
    logger.info(
        "Create column: project_id = %s user_id = %s",
        project_id,
        current_user.id
    )
    
    column = await db_add_column(
        project_id,
        session,
        data
    )

    logger.info(
        "Column created: project_id = %s column_id = %s user_id = %s",
        project_id,
        column.id,
        current_user.id
    )

    return column

@router.get(
    '',
    response_model=list[ResponseColumn]
)
async def get_columns(
    project_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_member)]
): 

    logger.info(
        "Get columns: project_id = %s user_id = %s",
        project_id,
        current_user.id
    )
    
    columns = await db_get_columns(
        project_id,
        session
    )

    logger.info(
        "Columns retrieved: project_id = %s count = %s user_id = %s",
        project_id,
        len(columns),
        current_user.id
    )

    return columns

@router.get(
    '/{column_id}',
    response_model=ResponseColumn
)
async def get_column(
    project_id: int,
    column_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_member)]
): 

    logger.info(
        "Get column: project_id = %s column_id = %s user_id = %s",
        project_id,
        column_id,
        current_user.id
    )
    
    column = await db_get_column(
        project_id,
        column_id,
        session
    )

    logger.info(
        "Column retrieved: proejct_id = %s column_id = %s user_id = %s",
        project_id,
        column.id,
        current_user.id
    )

    return column

@router.patch(
    '/{column_id}',
    response_model=ResponseColumn
)
async def update_column(
    project_id: int,
    column_id: int,
    session: SessionDep,
    data: UpdateColumn,
    current_user: Annotated[User, Depends(requier_project_manager)]
): 

    logger.info(
        "Update column: project_id = %s column_id = %s user_id = %s",
        project_id,
        column_id,
        current_user.id
    )
    
    column = await db_update_column(
        project_id,
        column_id,
        session,
        data
    )

    logger.info(
        "User updated: project_id = %s column_id = %s user_id = %s",
        project_id,
        column.id,
        current_user.id
    )

    return column

@router.delete(
    '/{column_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_column(
    project_id: int,
    column_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_manager)]
): 

    logger.info(
        "Delete column: project_id = %s column_id = %s user_id = %s",
        project_id,
        column_id,
        current_user.id
    )
    
    await db_delete_column(
        project_id,
        column_id,
        session
    )

    logger.info(
        "Column deleted: project_id = %s column_id = %s user_id = %s",
        project_id,
        column_id,
        current_user.id
    )