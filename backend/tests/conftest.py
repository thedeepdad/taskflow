from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from models import (
    User,
    Project,
    ProjectMember,
    Task,
    Column,
    Board,
    Comment,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from config import UserRole, TaskPriority, settings
from httpx import ASGITransport, AsyncClient
from config.database import get_session
from sqlalchemy import NullPool, text
from security import hash_password
from pathlib import Path
import pytest_asyncio
from main import app

@pytest_asyncio.fixture
async def session():
    test_engine = create_async_engine(
        settings.async_db_url,
        poolclass=NullPool,
    )

    session_factory = async_sessionmaker(
        test_engine,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        await session.execute(
            text("""
                TRUNCATE TABLE
                    project_members,
                    comments,
                    tasks,
                    columns,
                    boards,
                    projects,
                    users
                RESTART IDENTITY CASCADE
            """)
        )
        await session.commit()

        yield session

        await session.execute(
            text("""
                TRUNCATE TABLE
                    project_members,
                    comments,
                    tasks,
                    columns,
                    boards,
                    projects,
                    users
                RESTART IDENTITY CASCADE
            """)
        )
        await session.commit()

    await test_engine.dispose()

@pytest_asyncio.fixture
async def client(session):

    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(session):

    user = User(
        username="test_user",
        email="test_user1@example.com",
        password_hash=hash_password("password123"),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    yield user



@pytest_asyncio.fixture
async def test_user_without_delete(session): 
    user = User(
        username="test_user",
        email="test_user@gmail.com",
        password_hash=hash_password("password123")
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

@pytest_asyncio.fixture
async def test_proejcts_for_user(session, test_user): 
    projects = []

    for i in range(10): 
        project = Project(
            name=f"project_{i}",
            description=None,
            owner_id=test_user.id
        )

        session.add(project)
        await session.flush()

        member = ProjectMember(
            project_id=project.id,
            user_id=test_user.id,
            role=UserRole.admin
        )

        session.add(member)
        projects.append(project)

    await session.commit()

    yield projects



@pytest_asyncio.fixture
async def test_project(session, test_user):
    project = Project(
        name="TestProject",
        description=None,
        owner_id=test_user.id
    )

    session.add(project)
    await session.flush()

    member = ProjectMember(
        project_id=project.id,
        user_id=test_user.id,
        role=UserRole.admin
    )

    session.add(member)
    await session.commit()
    await session.refresh(project)

    yield project



@pytest_asyncio.fixture
async def test_board(session, test_project):
    board = Board(
        name="TestBoard",
        project_id=test_project.id
    )

    session.add(board)
    await session.commit()  
    await session.refresh(board)

    yield board



@pytest_asyncio.fixture
async def test_column(session, test_board): 
    column = Column(
        title="TestColumn",
        board_id=test_board.id
    )

    session.add(column)
    await session.commit()
    await session.refresh(column)

    yield column




@pytest_asyncio.fixture
async def test_task(session, test_project, test_column, test_user):
    task = Task(
        title="TestTask",
        description=None,
        priority=TaskPriority.medium,
        project_id=test_project.id,
        column_id=test_column.id,
        creator_id=test_user.id,
        assignee_id=None,
        due_date=None
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    yield task



@pytest_asyncio.fixture
async def test_tasks_for_user(session, test_project, test_column, test_user): 

    tasks = []

    for i in range(10):
        task = Task(
            title=f"TestTask_{i}",
            description=None,
            priority=TaskPriority.medium,
            project_id=test_project.id,
            column_id=test_column.id,
            creator_id=test_user.id,
            assignee_id=test_user.id,
            due_date=None
        )

        session.add(task)
        await session.flush()

        tasks.append(task)

    await session.commit()

    yield tasks




@pytest_asyncio.fixture
async def test_admin(session):
    admin = User(
        username="test_admin",
        email="admin@example.com",
        password_hash=hash_password("password123"),
        role=UserRole.admin
    )

    session.add(admin)
    await session.commit()
    await session.refresh(admin)

    yield admin



@pytest_asyncio.fixture
async def test_manager(session):
    manager = User(
        username="test_manager",
        email="manager@exmaple.com",
        password_hash=hash_password("password123"),
        role=UserRole.manager
    )

    session.add(manager)
    await session.commit()
    await session.refresh(manager)

    yield manager


@pytest_asyncio.fixture
async def test_member(session):
    user = User(
        username="test_member",
        email="test_member@example.com",
        password_hash=hash_password("password123"),
        role=UserRole.member
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    yield user


@pytest_asyncio.fixture
async def test_users_for_user(session): 
    users = []

    for i in range(10): 
        user = User(
            username=f"User_{i}",
            email=f"user_{i}@gmail.com",
            password_hash=hash_password("password123")
        )

        session.add(user)
        await session.flush()

        users.append(user)

    await session.commit()

    yield users


@pytest_asyncio.fixture
async def test_add_project(session): 
    user = User(
        username="testproject",
        email="testproject@gmail.com",
        password_hash=hash_password("password123"),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    yield user



@pytest_asyncio.fixture
async def test_add_board(session): 
    user = User(
        username="testboard",
        email="testboard@gmail.com",
        password_hash=hash_password("password123")
    )

    session.add(user)
    await session.flush()

    project = Project(
        name="TestProject",
        description=None,
        owner_id=user.id
    )

    session.add(project)
    await session.flush()

    project_member = ProjectMember(
        project_id=project.id,
        user_id=user.id,
        role=UserRole.manager
    )

    session.add(project_member)
    await session.flush()

    await session.commit()
    await session.refresh(user)
    await session.refresh(project)

    yield {
        "user": user,
        "project": project
    }



@pytest_asyncio.fixture
async def test_add_column(session):
    user = User(
        username="testcolumn",
        email="testcolumn@gmail.com",
        password_hash=hash_password("password123")
    )

    session.add(user)
    await session.flush()

    project = Project(
        name="TestProject",
        description=None,
        owner_id=user.id
    )

    session.add(project)
    await session.flush()

    project_member = ProjectMember(
        project_id=project.id,
        user_id=user.id,
        role=UserRole.manager
    )

    session.add(project_member)
    await session.flush()

    board = Board(
        name="TestBoard",
        project_id=project.id
    )

    session.add(board)
    await session.flush()

    await session.commit()
    await session.refresh(user)
    await session.refresh(project)

    yield {
        "user": user,
        "project": project,
        "board": board
    }


@pytest_asyncio.fixture
async def test_columns_for_users(session, test_board):
    columns = []

    for i in range(10):

        column = Column(
            title=f"Column_{i}",
            board_id=test_board.id,
            position=0
        )

        session.add(column)
        await session.flush()

        columns.append(column)

    await session.commit()

    yield columns


@pytest_asyncio.fixture
async def test_add_task(session): 
    user = User(
        username="testtask",
        email="testtask@gmail.com",
        password_hash=hash_password("password123")
    )

    session.add(user)
    await session.flush()

    project = Project(
        name="TestProject",
        description=None,
        owner_id=user.id
    )

    session.add(project)
    await session.flush()

    project_member = ProjectMember(
        project_id=project.id,
        user_id=user.id,
        role=UserRole.manager
    )

    session.add(project_member)
    await session.flush()

    board = Board(
        name="TestBoard",
        project_id=project.id
    )

    session.add(board)
    await session.flush()

    column = Column(
        title="TestColumn",
        board_id=board.id,
    )

    session.add(column)
    await session.flush()

    await session.commit()

    yield {
        "user": user,
        "project": project,
        "board": board,
        "column": column
    }

@pytest_asyncio.fixture
async def test_add_comment(session): 
    user = User(
        username="testtask",
        email="testtask@gmail.com",
        password_hash=hash_password("password123")
    )

    session.add(user)
    await session.flush()

    project = Project(
        name="TestProject",
        description=None,
        owner_id=user.id
    )

    session.add(project)
    await session.flush()

    project_member = ProjectMember(
        project_id=project.id,
        user_id=user.id,
        role=UserRole.manager
    )

    session.add(project_member)
    await session.flush()

    board = Board(
        name="TestBoard",
        project_id=project.id
    )

    session.add(board)
    await session.flush()

    column = Column(
        title="TestColumn",
        board_id=board.id,
    )

    session.add(column)
    await session.flush()

    task = Task(
        title="TestTask",
        description=None,
        priority="medium",
        assignee_id=None,
        project_id=project.id,
        column_id=column.id,
        creator_id=user.id
    )

    session.add(task)
    await session.flush()

    await session.commit()

    yield {
        "user": user,
        "project": project,
        "board": board,
        "column": column,
        "task": task
    }

@pytest_asyncio.fixture
async def test_comment(session, test_user, test_task):

    comment = Comment(
        text="TestComment",
        task_id=test_task.id,
        author_id=test_user.id
    )

    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    yield comment

@pytest_asyncio.fixture
async def test_comments_for_user(session, test_user, test_task): 

    comments = []

    for i in range(10):

        comment = Comment(
            text=f"comment_{i}",
            task_id=test_task.id,
            author_id=test_user.id
        )

        session.add(comment)
        await session.flush()

        comments.append(comment)

    await session.commit()

    yield comments
    
