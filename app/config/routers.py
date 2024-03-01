from fastapi import APIRouter
from app.apps.file.routers import router as file_router
from app.apps.auth.api.views import router as auth_router


urls = APIRouter()

urls.include_router(
    auth_router,
    prefix='/apps/auth',
    tags=[
        'auth',
    ]
)


urls.include_router(
    file_router,
    prefix='/apps/file',
    tags=[
        'file',
    ]
)

