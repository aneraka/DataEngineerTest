from jwt import encode, decode
from datetime import datetime, timedelta
from .settings import JWT_KEY
from .constants import JWT_ALGORITHM


def create_token(data: dict, key: str = JWT_KEY):
    return encode(
        payload=dict(
            expires_time=(datetime.now() + timedelta(minutes=60)).timestamp(),
            **data
        ),
        key=key,
        algorithm=JWT_ALGORITHM
    )


def validate_token(token: str, key: str = JWT_KEY) -> dict:
    return decode(
        jwt=token,
        key=key,
        algorithms=[JWT_ALGORITHM]
    )
