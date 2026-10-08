from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import (
    MappedAsDataclass, 
    DeclarativeBase
) 
from sqlalchemy import NullPool
from typing import Annotated
from fastapi import Depends
from config.settings import settings

class Base(MappedAsDataclass, DeclarativeBase): pass

engine = create_async_engine(
    url=settings.async_db_url,
    # poolclass=NullPool, нужна для тестов
)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False
)

async def get_session(): 
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)] 


