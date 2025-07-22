from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    include_in_schema= False
)

templates = Jinja2Templates(directory='templates/admin')


@router.get('/dashboard', response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse('layout.html', {'request': request})