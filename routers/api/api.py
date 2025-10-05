from fastapi import APIRouter
from infrastructure.tranaslations import TranslationManager



public_router = APIRouter(
    prefix='/api',
    tags=['api']
)
translation_manager = TranslationManager()