from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions.http import database_unvailable
from fastapi import HTTPException, status
from models import Register, User, Login
from sqlalchemy import select
from typing import Any
import logging 

db_logger = logging.getLogger('database')


async def add_user(
    session: AsyncSession,
    data: Register,
    hashed_password: str
) -> User: 

    db_logger.info(
        "Creating user started"
    )

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hashed_password
    )

    session.add(user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        db_logger.warning("DB integrity error while creating user")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this email or username already exists'
        )

    await session.refresh(user)

    db_logger.info(
        "User created: user_id = %s",
        user.id
    )

    return user

async def get_user(
    session: AsyncSession,
    data: Login | dict[str, Any]
) -> User: 

    db_logger.info(
        "Get user started"
    )

    if isinstance(data, dict):
        stmt = select(User).where(User.username == data.get('name'))
    else:
        stmt = select(User).where(User.username == data.username)

    try:
        user = await session.scalar(stmt)
    except OperationalError:
        db_logger.error("DB unvailable while getting user")
        await session.rollback()
        raise database_unvailable()


    if user is None:
        db_logger.warning("Login failed: user not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )

    db_logger.info(
        "User retrieved: user_id = %s",
        user.id
    )

    return user