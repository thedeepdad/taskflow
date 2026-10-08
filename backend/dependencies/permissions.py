from fastapi import (
    Depends, 
    status, 
    HTTPException
)
from exceptions.http import (
    requier_member,
    requier_project_access,
    comment_not_found,
    raise_forbidden, 
)
from config import SessionDep, UserRole
from models import User, ProjectMember, Comment
from sqlalchemy import select
from .auth import get_current_user
from typing import Annotated

def requier_role(*roles: str) -> function:

    async def checker(
        current_user: Annotated[User, Depends(get_current_user)]
    ) -> User:

        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Not enough permissions'
            )


        return current_user

    return checker

async def requier_project_manager(
    project_id: int,
    current_user: Annotated[
        User,
        Depends(get_current_user)
    ],
    session: SessionDep
) -> User: 

    stmt = select(ProjectMember)\
    .where(
        ProjectMember.user_id == current_user.id,
        ProjectMember.project_id == project_id
    )

    member = await session.scalar(stmt)

    if member is None:
        raise requier_project_access()

    if member.role not in (UserRole.admin, UserRole.manager):
        raise raise_forbidden()

    return current_user   

async def requier_project_member(
    project_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDep
): 

    stmt = select(ProjectMember)\
    .where(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    )

    member = await session.scalar(stmt)

    if member is None:
        raise requier_member()

    return current_user


async def requier_comment_owner_or_manager(
    comment_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDep
): 
    comment = await session.get(Comment, comment_id)

    if comment is None:
        raise comment_not_found()

    if (comment.author_id != current_user.id) and (current_user.role not in (UserRole.manager, UserRole.admin)):
        raise raise_forbidden()        

    return current_user
    