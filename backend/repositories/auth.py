from exceptions.http import (
    database_unvailable,
    user_not_found,
    registration_not_found
)
from models import Register, User, Login, RegistrationCode, VerifyEmail
from sqlalchemy.exc import IntegrityError, OperationalError
from security import generate_verification_code, hash_code, verify_code
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from rabbit.publisher import publish_email
from .common import execute_commit
from sqlalchemy import select
from typing import Any
import logging

db_logger = logging.getLogger('database')


async def add_user(
    session: AsyncSession,
    request: Request,
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
        await session.flush()

        code = generate_verification_code()

        registration_code = RegistrationCode(
            user_id=user.id,
            hash_code=hash_code(code),
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
        )

        session.add(registration_code)
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        db_logger.warning("DB integrity error while creating user")
        db_logger.exception("Integrity error: %s", exc.orig)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this email or username already exists'
        )

    await publish_email(
        channel=request.app.state.rabbit_channel,
        username=user.username,
        email=user.email,
        code=code
    )

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


async def db_verify_email(
    session: AsyncSession,
    data: VerifyEmail
):

    stmt = select(User).where(User.email == data.email)

    try:
        user = await session.scalar(stmt)
    except OperationalError:
        db_logger.error("DB unvailable while getting user")
        await session.rollback()
        raise database_unvailable()

    if user is None:
        raise user_not_found()

    stmt = select(RegistrationCode).where(RegistrationCode.user_id == user.id)

    try:
        registration_code = await session.scalar(stmt)
    except OperationalError:
        db_logger.error("DB unvailable while getting registration code")
        await session.rollback()
        raise database_unvailable()

    if registration_code is None:
        raise registration_not_found()

    if datetime.now(timezone.utc) >= registration_code.expires_at:
        await session.delete(registration_code)
        await session.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Registration code expired"
        )

    if registration_code.attempts >= 5:
        await session.delete(registration_code)
        await session.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Too many attempts"
        )

    if not verify_code(data.code, registration_code.hash_code):
        registration_code.attempts += 1
        await session.commit()
        db_logger.warning(
            "Verify code invalid"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Registration code invalid"
        )

    await session.delete(registration_code)

    await execute_commit(session)
