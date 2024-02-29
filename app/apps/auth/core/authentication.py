from .models import User
from fastapi import Request, status
from cryptography.fernet import Fernet
from ....config.settings import FERNET_KEY
from fastapi.security import HTTPBearer
from sqlalchemy.exc import NoResultFound
from ....config.connections import session_db
from fastapi.responses import HTMLResponse
from ....config.jwt_manager import validate_token
from jwt.exceptions import InvalidSignatureError


def get_user(username: str):
    with session_db() as session:
        try:
            user = session.query(User).filter(User.username == username).one()
            new_user = dict(
                username=user.username
            )
            new_user['password'] = Fernet(FERNET_KEY).decrypt(user.password.encode()).decode()
        except NoResultFound:
            new_user = None

        return new_user


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)

        try:
            data = validate_token(auth.credentials)
            user = get_user(data['username'])

        except InvalidSignatureError:
            user = None

        if user is None:
            return HTMLResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content="Credenciales Invalidas"
            )
