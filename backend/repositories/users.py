from models import (
    UpdateUser, 
    UpdateMe,
    Project, 
    User, 
    Task
)
from exceptions.http import (
    username_already_exists,
    email_already_exists,
    user_not_found,
)
from .common import execute_scalars, execute_commit
from config import SessionDep
from sqlalchemy import select, delete
import logging

db_logger = logging.getLogger('database')


async def db_get_all_users(
    session: SessionDep
) -> list[User]:

    db_logger.info(
        "Get users started"
    )

    result = await execute_scalars(
        session,
        select(User)
    )

    db_logger.info(
        "Users retrieved"
    )

    return result.all()


async def db_get_user(
    session: SessionDep,
    user_id: int
) -> User: 

    db_logger.info(
        "Get user started: user_id = %s",
        user_id
    )
    
    result = await session.get(User, user_id)

    if result is None:

        db_logger.warning(
            "User not found: user_id = %s",
            user_id
        )

        raise user_not_found()

    db_logger.info(
        "User retrieved: user_id = %s",
        user_id
    )

    return result


async def db_update_user(
    user_id: int,
    session: SessionDep,
    data: UpdateUser
) -> User: 

    db_logger.info(
        "Change user started: user_id = %s",
        user_id
    )

    user = await session.get(User, user_id)

    if user is None:

        db_logger.warning(
            "User not found: user_id = %s",
            user_id
        )

        raise user_not_found()

    if data.username is not None:
        stmt = select(User)\
        .where(
            User.username == data.username,
            User.id != user.id
        )

        result = await session.scalar(stmt)

        if result is not None:

            db_logger.warning(
                "Username already exists: user_id = %s",
                user_id
            )

            raise username_already_exists()

        user.username = data.username

    if data.email is not None:
        stmt = select(User)\
        .where(
            User.email == data.email,
            User.id != user.id
        )

        result = await session.scalar(stmt)

        if result is not None:

            db_logger.warning(
                "Email already exists: user_id = %s",
                user_id
            )

            raise email_already_exists()

        user.email = data.email

    if data.role is not None:
        user.role = data.role

    await execute_commit(session)

    await session.refresh(user)

    db_logger.info(
        "User changed successfully: user_id = %s",
        user_id
    )
    
    return user


async def db_delete_user(
    user_id: int,
    session: SessionDep
) -> None: 

    db_logger.info(
        "Delete user started: user_id = %s",
        user_id
    )
    
    stmt = delete(User)\
    .where(User.id == user_id)
    
    result = await session.execute(stmt)

    if result.rowcount == 0:
        await session.rollback()

        db_logger.warning(
            "User not found: user_id = %s",
            user_id
        )

        raise user_not_found()

    await execute_commit(session)

    db_logger.info(
        "User deleted: user_id = %s",
        user_id
    )


async def db_update_me(
    data: UpdateMe,
    session: SessionDep,
    user: User
) -> User: 

    db_logger.info(
        "Update user data started: user_id = %s",
        user.id
    )

    if data.username is not None:
        stmt = select(User)\
        .where(
            User.username == data.username,
            User.id != user.id
        )

        result = await session.scalar(stmt)

        if result is not None:

            db_logger.warning(
                "Username already exists"
            )

            raise username_already_exists()

        user.username = data.username

    if data.email is not None:
        stmt = select(User)\
        .where(
            User.email == data.email,
            User.id != user.id
        )

        result = await session.scalar(stmt)

        if result is not None:

            db_logger.warning(
                "Email already exists"
            )

            raise email_already_exists()

        user.email = data.email

    await execute_commit(session)

    await session.refresh(user)

    db_logger.info(
        "User data updated: user_id = %s",
        user.id
    )

    return user


async def db_delete_me(
    session: SessionDep,
    user: User
) -> None:

    db_logger.info(
        "Delete user started: user_id = %s",
        user.id
    )
     
    stmt = delete(User)\
    .where(User.id == user.id)

    result = await session.execute(stmt)

    if result.rowcount == 0:
        await session.rollback()
        
        db_logger.warning(
            "User not found: user_id = %s",
            user.id
        )

        raise user_not_found()
    
    await execute_commit(session)

    db_logger.info(
        "User deleted: user_id = %s",
        user.id
    )


async def db_get_projects_me(
    session: SessionDep,
    user: User
): 

    db_logger.info(
        "Get projects started: user_id = %s",
        user.id
    )
    
    stmt = select(Project)\
    .where(Project.owner_id == user.id)

    result = await execute_scalars(
        session,
        stmt
    )

    db_logger.info(
        "Projects retrieved: info = %s",
        user.id
    )

    return result.all()


async def db_get_tasks_me(
    session: SessionDep,
    user: User
): 

    db_logger.info(
        "Get project started: user_id = %s",
        user.id
    )
    
    stmt = select(Task)\
    .where(Task.assignee_id == user.id)

    tasks = await execute_scalars(
        session,
        stmt
    )

    db_logger.info("Project retrieved: user_id = %s", user.id)

    return tasks.all()
    