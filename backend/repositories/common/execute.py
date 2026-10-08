from config import SessionDep
from sqlalchemy.exc import OperationalError, IntegrityError
from exceptions.http import database_unvailable
import logging 

db_logger = logging.getLogger('database')

async def execute_scalars(
    session: SessionDep,
    stmt
): 
    try:
        result = await session.scalars(stmt)
    except OperationalError:
        db_logger.exception("Database unavailable")
        await session.rollback()
        raise database_unvailable()

    return result

async def execute_commit(
    session: SessionDep
): 
    try: 
        await session.commit()
    except IntegrityError:

        db_logger.error(
            "Database integrity error while changing user"
        )

        await session.rollback()
        raise database_unvailable()