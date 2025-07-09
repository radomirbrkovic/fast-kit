from fastapi import APIRouter

router = APIRouter(
    prefix='admin',
    tags=['admin'],
    include_in_schema= False
)