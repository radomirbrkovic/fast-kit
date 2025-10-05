from fastapi import APIRouter


public_router = APIRouter(
    prefix='/api',
    tags=['api']
)