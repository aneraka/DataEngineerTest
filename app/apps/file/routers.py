from fastapi import APIRouter
from .v1.api.views import router as file_router_v1



router = APIRouter()



file = APIRouter(
    prefix='/file/api/v1',
    tags=[
        'file',
    ]
)


file.include_router(
    file_router_v1
)


router.include_router(
    file
)

