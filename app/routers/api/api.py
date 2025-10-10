from fastapi import APIRouter, Depends
from app.infrastructure.tranaslations import TranslationManager
from app.middlewares.api_auth_middleware import auth
from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer()
public_router = APIRouter(
    prefix='/api',
    tags=['api']
)

guarded_router = APIRouter(
    prefix='/api',
    tags=['api'],
    dependencies=[Depends(auth), Depends(bearer_scheme)]
)

translation_manager = TranslationManager()