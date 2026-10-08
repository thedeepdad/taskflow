from fastapi import (
    HTTPException,
    APIRouter, 
    Response,
    Request, 
    status, 
    Form
)
from security import (
    verify_password,
    hash_password, 
    encode_token,
    decode_token
)
from models import (
    ResponseAuthMe,
    Register, 
    Login, 
)
from repositories import (
    get_user,
    add_user
)
from jwt.exceptions import InvalidTokenError
from config import SessionDep, Prefix, Tags
from typing import Annotated
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix=Prefix.auth, tags=[Tags.auth])


@router.post(
    '/register', 
    status_code=status.HTTP_201_CREATED
)
async def register(
    data: Annotated[Register, Form()],
    session: SessionDep,
    response: Response
) -> dict[str, str]: 

    logger.info("User register started")

    hashed_password = hash_password(data.password)

    user = await add_user(
        session,
        data,
        hashed_password
    )

    payload = {
        'sub': str(user.id),
        'name': user.username
    }

    access_token = encode_token(payload)
    refresh_token = encode_token(
        payload,
        refresh=True
    )

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        samesite='lax'
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        samesite='lax'        
    )

    logger.info("User registere successful")

    return {
        'message': 'user registered'
    }


@router.post('/login')
async def login(
    data: Annotated[Login, Form()],
    session: SessionDep,
    response: Response
) -> dict[str, str]: 

    logger.info("User login started")

    user = await get_user(session, data)

    if not verify_password(data.password, user.password_hash):
        logger.warning(
            "Username or password invalid"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid username or password'
        )

    payload = {
        'sub': str(user.id),
        'name': user.username
    }

    access_token = encode_token(payload)
    refresh_token = encode_token(
        payload,
        refresh=True
    )

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        samesite='lax'
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        samesite='lax'        
    )

    logger.info("User login successful")

    return {
        'message': 'user loged'
    }   


@router.post(
    '/refresh',
    status_code=status.HTTP_204_NO_CONTENT
)
async def refresh(
    request: Request,
    response: Response
) -> None: 

    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        logger.warning(
            "Token refresh failed: refresh token is missing"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token is missing'
        )
    
    try:
        refresh_payload = decode_token(refresh_token)
    except InvalidTokenError:
        logger.warning(
            "Token refresh failed: invalid refresh token"
        ) 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate refresh token'
        )

    logger.info(
        "Token refresh: username = %s",
        refresh_payload['sub']
    )

    payload = {
        'sub': refresh_payload.get('sub'),
        'name': refresh_payload.get('name')
    }


    access_token = encode_token(payload)
    refresh_token = encode_token(payload, refresh=True)

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        samesite='lax'
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        samesite='lax'
    )

    logger.info(
        "Token refresh successfull: username = %s",
        refresh_payload["sub"]
    )


@router.post(
    '/logout', 
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout(
    response: Response
) -> None:

    logger.info("User logout started")
    
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    logger.info("User logout successful")


@router.get('/me', response_model=ResponseAuthMe)
async def me(
    request: Request,
    session: SessionDep
) -> ResponseAuthMe: 

    logger.info("Get user data: request started")
    
    access_token = request.cookies.get('access_token')

    if not access_token:
        logger.warning("Get user data failed: access token missing")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )

    try:
        payload = decode_token(access_token)
    except InvalidTokenError:
        logger.warning("Get user data failed: invalid access token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )

    data = await get_user(session, payload)

    logger.info(
        "Get user data: user_id = %s",
        data.id 
    )  

    return data
