from models import (
    ResponseUpdateMember,
    ResponseProject,
    ResponseMembers,
    CreateProject,
    UpdateProject,
    UpdateMember,
    CreateMember,
    User
)
from repositories import (
    db_update_project,
    db_delete_project,
    db_delete_member,
    db_change_member,
    db_get_projects,
    db_get_members,
    db_get_project,
    db_add_project,
    db_add_member
)
from dependencies import (
    requier_project_manager,
    requier_project_member,
    get_current_user,
)
from config import SessionDep, Tags, Prefix, log_execute
from fastapi import APIRouter, Depends, status
from typing import Annotated
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=Prefix.projects,
    tags=[Tags.projects]
)


@log_execute
@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseProject
)
async def add_project(
    data: CreateProject,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)]
) -> ResponseProject:

    project = await db_add_project(
        data,
        session,
        current_user
    )

    return project


@log_execute
@router.get(
    '',
    response_model=list[ResponseProject]
)
async def get_projects(
    session: SessionDep,
    _: Annotated[User, Depends(get_current_user)]
) -> list[ResponseProject]:

    projects = await db_get_projects(session)

    return projects


@log_execute
@router.get(
    '/{project_id}',
    response_model=ResponseProject
)
async def get_project(
    project_id: int,
    session: SessionDep,
    _: Annotated[
        User,
        Depends(requier_project_member)
    ]
) -> ResponseProject:

    project = await db_get_project(
        project_id,
        session
    )

    return project


@log_execute
@router.patch(
    '/{project_id}',
    response_model=ResponseProject
)
async def update_project(
    project_id: int,
    data: UpdateProject,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_manager)]
) -> ResponseProject:

    project = await db_update_project(
        project_id,
        data,
        session
    )

    return project


@log_execute
@router.delete(
    '/{project_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_project(
    project_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_manager)]
) -> None:

    await db_delete_project(
        project_id,
        session
    )


@log_execute
@router.get(
    '/{project_id}/members',
    response_model=list[ResponseMembers]
)
async def get_members(
    project_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_member)]
) -> list[ResponseMembers]:

    result = await db_get_members(
        project_id,
        session,
    )

    return result


@log_execute
@router.post(
    '/{project_id}/members',
    status_code=status.HTTP_201_CREATED
)
async def add_members(
    project_id: int,
    session: SessionDep,
    data: CreateMember,
    current_user: Annotated[User, Depends(requier_project_manager)]
) -> dict[str, str]:

    await db_add_member(
        project_id,
        session,
        data,
        current_user
    )

    return {
        'message': 'user added'
    }


@log_execute
@router.patch(
    '/{project_id}/members/{user_id}',
    response_model=ResponseUpdateMember
)
async def change_member(
    project_id: int,
    user_id: int,
    session: SessionDep,
    data: UpdateMember,
    _: Annotated[User, Depends(requier_project_manager)]
):

    member = await db_change_member(
        project_id,
        user_id,
        session,
        data
    )

    return member


@log_execute
@router.delete(
    '/{project_id}/members/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_member(
    project_id: int,
    user_id: int,
    session: SessionDep,
    _: Annotated[User, Depends(requier_project_manager)]
) -> None:

    await db_delete_member(
        project_id,
        user_id,
        session
    )
