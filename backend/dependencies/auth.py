from fastapi import (
    HTTPException,
    Request,
    status, 
)
from jwt.exceptions import InvalidTokenError
from config import SessionDep
from security import decode_token
from models import User

async def get_current_user(
    session: SessionDep,
    request: Request
) -> User: 

    access_token = request.cookies.get('access_token')

    if not access_token: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated'
        )

    try:
        payload = decode_token(access_token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )

    user_id = payload.get('sub')

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )

    user = await session.get(User, int(user_id))

    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found'
        )

    return user


    