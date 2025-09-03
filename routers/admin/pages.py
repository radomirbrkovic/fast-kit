from fastapi import Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional

from schemas.admin.pages import PageCreate
from services.admin.page_service import PageService
from repositories.admin.page_repository import PageRepository
from routers.admin.admin import guard_router, get_db, templates
from sqlalchemy.orm import Session

router = guard_router

def get_service(db: Session = Depends(get_db)):
    return PageService(PageRepository(db))

@router.get('/pages', response_class=HTMLResponse, name='admin.pages.index')
async  def index(request: Request, page: Optional[int] = 1, services: PageService = Depends(get_service)):
    pages = services.get({'page': page})
    return templates.TemplateResponse('pages/index.html', {'request': request, 'pages': pages})

@router.get('/pages/create', response_class=HTMLResponse, name='admin.pages.create')
async def create(request: Request):
    return templates.TemplateResponse('pages/create.html', {'request': request})

@router.post('/pages', response_class=HTMLResponse, name='admin.pages.store')
async def store(request: Request, service: PageService = Depends(get_service)):
    try:
        form = await request.form()
        form_data = dict(form)
        page_data = PageCreate(**form_data)
        service.create(page_data)
        return RedirectResponse(url="/admin/pages", status_code=302)
    except ValueError as e:
        return templates.TemplateResponse('pages/create.html', {'request': request, 'error_msg': str(e)})