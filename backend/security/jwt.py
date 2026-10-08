from datetime import datetime, timedelta, timezone
from typing import Any
from jwt import encode, decode
from config import settings

def encode_token(
    payload: dict[str, Any], 
    refresh: bool = False
) -> str: 

    if refresh:
        exp = timedelta(days=settings.refresh_token_exp)
        token_type = 'refresh'
    else:
        exp = timedelta(minutes=settings.access_token_exp)
        token_type = 'access'


    time_now = datetime.now(timezone.utc)
    payload_update = {
        'iat': time_now,
        'exp': time_now + exp,
        'type': token_type
    }

    payload.update(payload_update)

    token = encode(
        payload=payload,
        key=settings.private_key,
        algorithm=settings.algorithm
    )

    return token

def decode_token(token: str | bytes) -> dict[str, Any]: 

    payload = decode(
        jwt=token,
        key=settings.public_key,
        algorithms=[settings.algorithm]
    )

    return payload

