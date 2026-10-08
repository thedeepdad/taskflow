from models import (
    CreateProject,
    UpdateProject, 
    ProjectMember,
    CreateMember,
    UpdateMember,
    Project, 
    User
) 
from exceptions.http import (
    member_already_exists,
    project_not_found, 
    user_not_found, 
    member_not_found,
)
from config import SessionDep, UserRole
from .common import execute_commit, execute_scalars
from sqlalchemy import select, delete
import logging

db_logger = logging.getLogger('database')

async def db_add_project(
    data: CreateProject,
    session: SessionDep,
    user: User
) -> Project: 

    db_logger.info(
        "Create project started: user_id = %s",
        user.id
    )

    project = Project(
        name=data.name,
        description=data.description,
        owner_id=user.id
    )

    session.add(project)

    await session.flush()

    member = ProjectMember(
        project_id=project.id,
        user_id=user.id,
        role=UserRole.admin
    )

    session.add(member)

    await execute_commit(session)

    await session.refresh(project)

    db_logger.info(
        "Project created: project_id = %s user_id = %s",
        project.id,
        user.id
    )

    return project


async def db_get_projects(
    session: SessionDep,
) -> list[Project]: 

    db_logger.debug(
        "Get projects started"
    )

    result = await execute_scalars(
        session,
        select(Project)
    )

    db_logger.debug(
        "Projects retrieved successfuly"
    )

    return result.all()

async def db_get_project(
    project_id: int,
    session: SessionDep,
) -> Project:

    db_logger.info("Get proeject started: project_id = %s", project_id)
     
    stmt = select(Project)\
    .where(Project.id == project_id)

    project = await session.scalar(stmt)

    if project is None:

        db_logger.warning("Project not found: project_id = %s", project_id)

        raise project_not_found()

    db_logger.info("Project retrieved: project_id = %s", project_id)

    return project

async def db_update_project(
    project_id: int,
    data: UpdateProject,
    session: SessionDep,
): 

    db_logger.info("Update project started: project_id = %s", project_id)

    stmt = select(Project)\
    .where(Project.id == project_id)

    project = await session.scalar(stmt)

    if project is None:

        db_logger.warning("Project not found: project_id = %s", project_id)

        raise project_not_found()
    
    if data.name is not None:
        project.name = data.name
    if data.description is not None:
        project.description = data.description

    await execute_commit(session)
    
    await session.refresh(project)

    db_logger.info("Project updated: project_id = %s", project_id)

    return project

async def db_delete_project(
    project_id: int,
    session: SessionDep
) -> None:

    db_logger.info("Delete project started: project_id = %s", project_id)
    
    stmt = delete(Project).where(Project.id == project_id)
    result = await session.execute(stmt)

    if result.rowcount == 0:
        await session.rollback()

        db_logger.warning("Project not found: project_id = %s", project_id)

        raise project_not_found()

    await execute_commit(session)
    
    db_logger.info("Project deleted: project_id = %s", project_id)

async def db_get_members(
    project_id: int,
    session: SessionDep,
):

    db_logger.info("Get members started: project_id = %s", project_id)

    stmt = select(User)\
    .join(ProjectMember, ProjectMember.user_id == User.id)\
    .where(ProjectMember.project_id == project_id)

    result = await execute_scalars(
        session,
        stmt
    )

    db_logger.info("Members retrieved: project_id = %s", project_id)

    return result.all()

async def db_add_member(
    project_id: int,
    session: SessionDep,
    data: CreateMember,
    user: User
): 

    db_logger.info("Add member started: project_id = %s user_id = %s",
        project_id,
        user.id
    )

    stmt = select(User)\
    .where(User.username == data.username)

    user = await session.scalar(stmt)

    if user is None: 

        db_logger.warning(
            "User not found: project_id = %s user_id = %s",
            project_id,
            user.id
        )

        raise user_not_found()

    stmt = select(ProjectMember)\
    .where(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id
    )

    member = await session.scalar(stmt)

    if member is not None:

        db_logger.warning(
            "Member already exists: project_id = %s user_id = %s",
            project_id,
            user.id
        )

        raise member_already_exists()

    project_member = ProjectMember(
        project_id=project_id,
        user_id=user.id
    )

    if data.role is not None:
        project_member.role = data.role

    session.add(project_member)

    await execute_commit(session)

    db_logger.info(
        "Member added: project_id = %s member_user_id = %s user_id = %s",
        project_id,
        project_member.user_id,
        user.id
    )

async def db_delete_member(
    project_id: int,
    user_id: int,
    session: SessionDep
): 

    db_logger.info(
        "Delete member started: project_id = %s user_id = %s",
        project_id,
        user_id
    )

    stmt = delete(ProjectMember)\
    .where(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    )

    result = await session.execute(stmt)
    await execute_commit(session)

    if result.rowcount == 0:

        db_logger.warning(
            "Member not found: user_id = %s",
            user_id
        )

        raise member_not_found()

    db_logger.info(
        "Member deleted: project_id = %s user_id = %s",
        project_id,
        user_id
    )

async def db_change_member(
    project_id: int, 
    user_id: int,
    session: SessionDep,
    data: UpdateMember
): 

    db_logger.info(
        "Change member started: project_id = %s user_id = %s",
        project_id,
        user_id
    )

    stmt = select(ProjectMember)\
    .where(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    )

    member = await session.scalar(stmt)

    if member is None:

        db_logger.warning(
            "Member not found: project_id = %s user_id = %s",
            project_id,
            user_id
        )

        raise member_not_found()

    if data.role is not None:
        member.role = data.role

    await execute_commit(session)

    await session.refresh(member)

    db_logger.info(
        "Member changed: project_id = %s user_id = %s",
        project_id,
        user_id
    )

    return member