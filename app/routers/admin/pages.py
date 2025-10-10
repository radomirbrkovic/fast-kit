from fastapi import Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional

from app.schemas.admin.pages import PageCreate, PageUpdate
from app.services.admin.page_service import PageService
from app.repositories.admin.page_repository import PageRepository
from app.routers.admin.admin import guard_router, get_db, templates
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

@router.get('/pages/{id}/edit', response_class=HTMLResponse, name='admin.pages.edit')
async def edit(id: int, request: Request, service: PageService = Depends(get_service)):
    page = service.find(id)
    return templates.TemplateResponse('pages/edit.html', {'request': request, 'page': page})

@router.post('/pages/{id}', response_class=HTMLResponse, name='admin.pages.update')
async def update(id:int, request: Request, service: PageService = Depends(get_service)):
    try:
        form = await request.form()
        form_data = dict(form)
        page_data = PageUpdate(**form_data)
        service.update(id, page_data)
        return RedirectResponse(url="/admin/pages", status_code=302)
    except ValueError as e:
        page = service.find(id)
        return templates.TemplateResponse('pages/edit.html', {'request': request, 'page': page, 'error_msg': str(e)})

@router.delete('/pages/{id}', name='admin.pages.delete')
async def delete(id: int, service: PageService = Depends(get_service)):
    service.delete(id)
    return {"message": 'Page has been successfully deleted.'}