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
    log_execute,
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


@log_execute
@router.get(
    '/me',
    response_model=ResponseMe
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


@log_execute
@router.patch('/me', response_model=ResponseMe)
async def update_me(
    data: UpdateMe,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
):

    user = await db_update_me(
        data,
        session,
        current_user
    )

    return user


@log_execute
@router.delete(
    '/me',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_me(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
) -> None:

    await db_delete_me(
        session,
        current_user
    )


@log_execute
@router.get(
    '/me/projects',
    response_model=list[ResponseProject]
)
async def get_projects(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
) -> list[ResponseProject]:

    projects = await db_get_projects_me(
        session,
        current_user
    )

    return projects


@log_execute
@router.get(
    '/me/tasks',
    response_model=list[ResponseTask]
)
async def get_tasks(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
) -> list[ResponseTask]:

    tasks = await db_get_tasks_me(
        session,
        current_user
    )

    return tasks


@log_execute
@router.get(
    '',
    response_model=list[UserSchema]
)
async def get_users(
    session: SessionDep,
    _: Annotated[User, Depends(requier_role(UserRole.admin))]
) -> list[UserSchema]:

    users = await db_get_all_users(session)

    return users


@log_execute
@router.get(
    '/{user_id}',
    response_model=UserSchema
)
async def get_user(
    user_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_role(UserRole.admin))]
) -> User:

    user = await db_get_user(session, user_id)

    return user


@log_execute
@router.patch(
    '/{user_id}',
    response_model=UserSchema
)
async def update_user(
    user_id: int,
    session: SessionDep,
    data: UpdateUser,
    _: Annotated[User, Depends(requier_role(UserRole.admin))],
) -> User:

    user = await db_update_user(
        user_id,
        session,
        data
    )

    return user


@log_execute
@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    user_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_role(UserRole.admin))]
) -> None:

    await db_delete_user(user_id, session)
