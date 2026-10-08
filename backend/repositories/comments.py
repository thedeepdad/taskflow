from models import (
    UpdateComment,
    CreateComment,
    Comment, 
    User,
)
from .common import (
    validation_comment, 
    execute_commit, 
    execute_scalars
)
from exceptions.http import comment_not_found
from config import SessionDep
from sqlalchemy import select, delete
import logging

db_logger = logging.getLogger('database')

async def db_add_comment(
    project_id: int,
    column_id: int,
    task_id: int,
    data: CreateComment,
    session: SessionDep, 
    user: User
): 

    db_logger.info(
        "Create comment started: project_id = %s column_id = %s task_id = %s user_id = %s",
        project_id,
        column_id,
        task_id,
        user.id
    )
    
    await validation_comment(
        project_id,
        column_id,
        task_id,
        session
    )

    comment = Comment(
        text=data.text,
        task_id=task_id,
        author_id=user.id
    )

    session.add(comment)

    await execute_commit(session)
    await session.refresh(comment)

    db_logger.info(
        "Comment created: project_id = %s column_id = %s task_id = %s user_id = %s",
        project_id,
        column_id,
        task_id,
        user.id
    )

    return comment

async def db_get_comments(
    project_id: int,
    column_id: int,
    task_id: int,
    session: SessionDep,
    user: User
): 

    db_logger.info(
        "Get comments started: project_id = %s column_id = %s task_id = %s user_id = %s",
        project_id,
        column_id,
        task_id,
        user.id
    )
    
    await validation_comment(
        project_id,
        column_id,
        task_id,
        session
    )

    stmt = select(Comment)\
    .where(
        Comment.task_id == task_id,
        Comment.author_id == user.id
    )

    comment = await execute_scalars(session, stmt)

    db_logger.info(
        "Comments retrieved: project_id = %s column_id = %s task_id = %s user_id = %s",
        project_id,
        column_id,
        task_id,
        user.id
    )

    return comment.all()


async def db_get_comment(
    project_id: int,
    column_id: int,
    task_id: int,
    comment_id: int,
    session: SessionDep,
): 

    db_logger.info(
        "Get comment started: project_id = %s column_id = %s task_id = %s comment_id = %s",
        project_id,
        column_id,
        task_id,
        comment_id
    )

    await validation_comment(
        project_id,
        column_id,
        task_id,
        session,
    )

    stmt = select(Comment)\
    .where(
        Comment.id == comment_id
    )

    comment = await session.scalar(stmt)

    if comment is None:

        db_logger.warning(
            "Comment not found: project_id = %s column_id = %s task_id = %s comment_id = %s",
            project_id,
            column_id,
            task_id,
            comment_id
        )

        raise comment_not_found()

    db_logger.info(
        "Comment retrieved: project_id = %s column_id = %s task_id = %s comment_id = %s",
            project_id,
            column_id,
            task_id,
            comment_id
        )

    return comment    

async def db_update_comment(
    project_id: int,
    column_id: int,
    task_id: int,
    comment_id: int,
    data: UpdateComment,
    session: SessionDep,
): 

    db_logger.info(
        "Update comment started: project_id = %s column_id = %s task_id = %s comment_id = %s",
        project_id,
        column_id,
        task_id,
        comment_id
    )

    await validation_comment(
        project_id,
        column_id,
        task_id,
        session
    )

    stmt = select(Comment)\
    .where(
        Comment.id == comment_id
    )

    comment = await session.scalar(stmt)

    if comment is None:

        db_logger.warning(
            "Comment not found: project_id = %s column_id = %s task_id = %s comment_id = %s",
            project_id,
            column_id,
            task_id,
            comment_id
        )

        raise comment_not_found()

    if data.text is not None:
        comment.text = data.text

    await execute_commit(session)
    await session.refresh(comment)

    db_logger.info(
        "Comment updated successfuly: project_id = %s column_id = %s task_id = %s comment_id = %s",
            project_id,
            column_id,
            task_id,
            comment_id
        )

    return comment

async def db_delete_comment(
    project_id: int,
    column_id: int,
    task_id: int,
    comment_id: int,
    session: SessionDep, 
): 

    db_logger.info(
        "Delete comment started: project_id = %s column_id = %s task_id = %s comments_id = %s",
            project_id,
            column_id,
            task_id,
            comment_id
        )

    await validation_comment(
        project_id,
        column_id,
        task_id,
        session
    )

    stmt = delete(Comment)\
    .where(
        Comment.id == comment_id
    )

    result = await session.execute(stmt)
    await execute_commit(session)

    if result.rowcount == 0:

        db_logger.warning(
            "Comment not found: project_id = %s column_id = %s task_id = %s comments_id = %s",
            project_id,
            column_id,
            task_id,
            comment_id
        )

        raise comment_not_found()

    db_logger.info(
        "Comment deleted: project_id = %s column_id = %s task_id = %s comments_id = %s",
            project_id,
            column_id,
            task_id,
            comment_id
        )