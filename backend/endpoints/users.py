from models import (
    ResponseTask,
    ResponseProject,
    UserSchema,
    UpdateUser,
    ResponseMe,
    UpdateMe,
    User,
)
from repositories import (
    db_get_projects_me,
    db_get_tasks_me,
    db_get_all_users,
    db_delete_user,
    db_update_user,
    db_delete_me,
    db_get_user,
    db_update_me
)
from fastapi import (
    APIRouter, 
    Depends, 
    status
)
from dependencies import (
    requier_role, 
    get_current_user
)
from config import (
    SessionDep, 
    UserRole, 
    Prefix, 
    Tags,
)
from typing import Annotated
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=Prefix.users,
    tags=[Tags.users]
)

@router.get(
    '/me', 
    response_model=ResponseMe
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)]
): 

    logger.info("User requested their profile: user_id = %s",
        current_user.id
    )
    
    return current_user

@router.patch('/me', response_model=ResponseMe)
async def update_me(
    data: UpdateMe,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
):  

    logger.info(
        "User update: user_id = %s",
        current_user.id
    )
    
    user = await db_update_me(
        data,
        session,
        current_user
    )

    logger.info(
        "User updated: user_id = %s",
        current_user.id
    )

    return user

@router.delete(
    '/me', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_me(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
) -> None: 

    logging.info("User delete: user_id = %s",
        current_user.id
    )

    await db_delete_me(
        session,
        current_user
    )

    logger.info("User deleted: user_id = %s",
        current_user.id
    )



@router.get(
    '/me/projects',
    response_model=list[ResponseProject]
)      
async def get_projects(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
) -> list[ResponseProject]: 
        
    logger.info(
        "Get projects: user_id = %s",
        current_user.id
    )   
    
    projects = await db_get_projects_me(
        session,
        current_user
    )

    logger.info(
        "Projects retrieved: count = %s user_id = %s",
        len(projects),
        current_user.id
    )

    return projects

@router.get(
    '/me/tasks',
    response_model=list[ResponseTask]
)
async def get_tasks(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
) -> list[ResponseTask]: 

    logger.info(
        "Get tasks: user_id = %s",
        current_user.id
    )

    tasks = await db_get_tasks_me(
        session,
        current_user
    )

    logger.info(
        "Tasks retrieved: count = %s user_id = %s",
        len(tasks),
        current_user.id
    )

    return tasks


@router.get(
    '',
    response_model=list[UserSchema]
)
async def get_users(
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_role(UserRole.admin))]
) -> list[UserSchema]: 

    logger.info(
        "Get users: user_id = %s",
        current_user.id
    )

    users = await db_get_all_users(session)

    logger.info(
        "Users retrieved: count = %s user_id = %s",
        len(users),
        current_user.id
    )

    return users

@router.get(
    '/{user_id}',
    response_model=UserSchema
)
async def get_user(
    user_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_role(UserRole.admin))]
) -> User: 
    
    logger.info(
        "Get user: member_id = %s by_user_id = %s",
        user_id,
        current_user.id
    )

    user = await db_get_user(session, user_id)

    logger.info(
        "User retrieved: member_id = %s by_user_id = %s",
        user_id,
        current_user.id
    )

    return user

@router.patch(
    '/{user_id}',
    response_model=UserSchema
)
async def update_user(
    user_id: int, 
    session: SessionDep,
    data: UpdateUser,
    current_user: Annotated[User, Depends(requier_role(UserRole.admin))],
) -> User: 

    logger.info(
        "Update user: member_id = %s user_id = %s",
        user_id,
        current_user.id
    )

    user = await db_update_user(
        user_id,
        session,
        data
    )

    logger.info(
        "User updated: member_id = %s user_id = %s"
    )

    return user  

@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    user_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_role(UserRole.admin))]
) -> None:

    logger.info(
        "User delete: member_id = %s user_id = %s",
        user_id,
        current_user.id
    )

    await db_delete_user(user_id, session)

    logger.info(
        "Deleted user: member_id = %s user_id = %s",
        user_id,
        current_user.id
    )
