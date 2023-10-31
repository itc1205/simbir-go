from datetime import timedelta, datetime
from typing import Optional

from jose import jwt, JWTError

from simbir_go_backend.config import (
    get_secret_key,
    get_algorithm,
    get_token_expire_minutes,
)


# We could use redis to store banned tokens, but for now, we will use set
banned_tokens = set()


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(get_token_expire_minutes())

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, get_secret_key(), algorithm=get_algorithm())

    return encoded_jwt


def ban_token(token: str):
    banned_tokens.add(token)


def check_if_token_banned(token: str) -> bool:
    # Function for checking if token is not banned
    return token in banned_tokens


def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=[get_algorithm()])
    except JWTError:
        return None
    username = payload.get("sub")
    return username
