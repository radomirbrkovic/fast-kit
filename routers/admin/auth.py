from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from models.enums import UserRole
from routers.admin.admin import router, templates
from services.auth_service import AuthService

auth_service = AuthService()


@router.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse('sign-in.html', {"request": request})

@router.post('/login', response_class=HTMLResponse)
async def authenticate(request: Request, email: str = Form(), password: str= Form()):
    user = auth_service.authenticate(email, password, UserRole.SUPER_ADMIN)

    if user is None:
        return templates.TemplateResponse('sign-in.html', {"request": request, 'error_msg': "Invalid credentials."})
    else:
        request.session['auth_id'] = user.id
        request.session['auth_name'] = user.first_name
        return templates.TemplateResponse('sign-in.html', {"request": request, 'error_msg': "User successfully authenticated."})