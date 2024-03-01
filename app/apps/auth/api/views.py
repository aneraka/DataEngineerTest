from fastapi import APIRouter, status
from .serializers import UserSerializer
from ..core.authentication import get_user
from fastapi.responses import JSONResponse
from ....config.jwt_manager import create_token

router = APIRouter(
    prefix='/auth',
    tags=[
        'auth'
    ]
)


@router.post('/login', tags=['auth'])
async def login(user: UserSerializer):
    db_user = get_user(user.username)

    if db_user is not None and user.password == db_user['password']:
        token: str = create_token(db_user)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=token
        )

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content='Validate user and password'
    )
