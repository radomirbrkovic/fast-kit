from fastapi import Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from routers.admin.admin import guard_router, templates, get_db
from repositories.admin.user_repository import UserRepository
from services.admin.user_service import UserService
from sqlalchemy.orm import Session
from models.enums import UserRole
from schemas.admin.users import UserCreate

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
    return templates.TemplateResponse('users/create.html', {'request': request, 'roles': list(UserRole)})

@router.post('/users', response_class=HTMLResponse, name='admin.users.store')
async  def store(request: Request, db: Session = Depends(get_db), service: UserService = Depends(get_service)):
    try:
        form = await request.form()
        form_data = dict(form)
        user_data = UserCreate(**form_data, db_session=db)
        UserCreate.validate_unique_email(user_data.email, db)
        service.create(user_data)
        return RedirectResponse(url="/admin/users", status_code=302)
    except ValueError as e:
        return templates.TemplateResponse('users/create.html', {'request': request, 'roles': list(UserRole), 'error_msg': str(e)})