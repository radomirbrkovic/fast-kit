from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from middlewares.admin_middleware import auth

public_router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    include_in_schema= False
)

guard_router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    include_in_schema= False,
    dependencies=[Depends(auth)]
)

templates = Jinja2Templates(directory='templates/admin')