from fastapi import APIRouter
from app.apps.auth.api.views import router as auth_router


urls = APIRouter()

urls.include_router(
    auth_router,
    prefix='/apps/auth',
    tags=[
        'auth',
    ]
)
