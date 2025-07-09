from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    include_in_schema= False
)

templates = Jinja2Templates(directory='templates/admin')