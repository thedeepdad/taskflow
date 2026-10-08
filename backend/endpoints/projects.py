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
from config import SessionDep, Tags, Prefix
from fastapi import APIRouter, Depends, status
from typing import Annotated
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix=Prefix.projects, 
    tags=[Tags.projects]
)

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

    logger.info(
        "Creating project: user_id = %s",
        current_user.id
    )

    project = await db_add_project(
        data,
        session,
        current_user
    )   
    
    logger.info(
        "Project created: project_id = %s, user_id = %s",
        project.id,
        current_user.id
    )

    return project

@router.get(
    '',
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
    
    projects = await db_get_projects(session)

    logger.info(
        "Projects retrieved: count = %s, user_id = %s",
        len(projects),
        current_user.id
    )

    return projects

@router.get(
    '/{project_id}', 
    response_model=ResponseProject
)
async def get_project(
    project_id: int,
    session: SessionDep,
    current_user: Annotated[
        User, 
        Depends(requier_project_member)
    ]
) -> ResponseProject: 

    logger.info(
        "Get proeject: user_id = %s", 
        current_user.id
    )
    
    project = await db_get_project(
        project_id,
        session
    )

    logger.info(
        "Project retrieved project_id = %s user_id = %s",
        project.id,
        current_user.id
    )

    return project 

@router.patch(
    '/{project_id}',
    response_model=ResponseProject
)
async def update_project(
    project_id: int, 
    data: UpdateProject,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_manager)]
) -> ResponseProject: 

    logger.info(
        "Update project: user_id = %s",
        current_user.id
    )

    project = await db_update_project(
        project_id, 
        data, 
        session
    )

    logger.info(
        "Project updated: project_id = %s user_id = %s",
        project_id,
        current_user.id
    )

    return project

   

@router.delete(
    '/{project_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_project(
    project_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_manager)]
) -> None: 

    logger.info(
        "Delete project: user_id = %s",
        current_user.id
    )
    
    await db_delete_project(
        project_id, 
        session
    )

    logger.info(
        "Project deleted: project_id = %s user_id = %s",
        project_id,
        current_user.id
    )


@router.get(
    '/{project_id}/members',
    response_model=list[ResponseMembers]
)
async def get_members(
    project_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_member)]
) -> list[ResponseMembers]: 

    logger.info("Get members in project: project_id = %s user_id = %s",
        project_id,
        current_user.id
    )
    
    result = await db_get_members(
        project_id,
        session,
    )

    logger.info("Members retrieved: project_id = %s user_id = %s",
        project_id,
        current_user.id
    )

    return result
    

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

    logger.info("Add member started: project_id = %s user_id = %s",
        project_id, 
        current_user.id
    )
    
    await db_add_member(
        project_id,
        session,
        data,
        current_user
    )

    logger.info("Member added: project_id = %s user_id = %s",
        project_id,
        current_user.id
    )

    return {
        'message': 'user added'
    }

@router.patch(
    '/{project_id}/members/{user_id}',
    response_model=ResponseUpdateMember
)
async def change_member(
    project_id: int,
    user_id: int,   
    session: SessionDep,
    data: UpdateMember,
    current_user: Annotated[User, Depends(requier_project_manager)]
): 

    logger.info("Change member: project_id = %s member_id = %s by_user_id = %s",
        project_id,
        user_id,
        current_user.id
    )

    member = await db_change_member(
        project_id,
        user_id,
        session,
        data
    )

    logger.info("Member changed: project_id = %s member_id = %s by_user_id = %s",
        project_id,
        user_id,
        current_user.id
    )

    return member

@router.delete(
    '/{project_id}/members/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_member(
    project_id: int,
    user_id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(requier_project_manager)]
) -> None: 

    logger.info(
        "Delete member: project_id = %s member_id = %s by_user_id = %s", 
        project_id,
        user_id,
        current_user.id
    )
    
    await db_delete_member(
        project_id,
        user_id,
        session
    )

    logger.info(
        "Member deleted: project_id = %s member_id = %s by_user_id = %s",
        project_id,
        user_id,   
        current_user.id
    )