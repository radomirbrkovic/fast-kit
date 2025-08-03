from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from typing import Optional
from routers.admin.admin import guard_router, templates, get_db
from repositories.admin.user_repository import UserRepository
from services.admin.user_service import UserService
from sqlalchemy.orm import Session

router = guard_router

def get_service(db: Session = Depends(get_db)):
    return UserService(UserRepository(db))

@router.get('/users', response_class=HTMLResponse, name="admin.users.index")
async def index(
        request: Request,
        query: Optional[str]= "",
        page: Optional[int] = 1,
        service: UserService = Depends(get_service)):
    users = service.get({'query': query, 'page': page})
    return templates.TemplateResponse('users/index.html', {'request': request, 'query': query, 'users': users})

@router.get('/users/create', response_class=HTMLResponse, name='admin.users.create')
async def create(request: Request):
    return templates.TemplateResponse('users/create.html', {'request': request})