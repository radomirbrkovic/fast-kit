from fastapi import Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError
from models.enums import UserRole
from repositories.admin.user_repository import UserRepository
from repositories.admin.user_token_repository import UserTokenRepository
from routers.admin.admin import public_router, templates, get_db
from schemas.admin.auth import ResetPasswordSchema
from services.admin.user_service import UserService
from services.admin.user_token_service import UserTokenService
from services.auth_service import AuthService
from sqlalchemy.orm import Session

auth_service = AuthService()
router = public_router

def get_user_token_service(db: Session = Depends(get_db)):
    return UserTokenService(UserTokenRepository(db))

def get_user_tservice(db: Session = Depends(get_db)):
    return UserService(UserRepository(db))

@router.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse('auth/sign-in.html', {"request": request})

@router.post('/login', response_class=HTMLResponse)
async def authenticate(request: Request, email: str = Form(), password: str= Form()):
    user = auth_service.authenticate(email, password, UserRole.SUPER_ADMIN)

    if user is None:
        return templates.TemplateResponse('auth/sign-in.html', {"request": request, 'error_msg': "Invalid credentials."})
    else:
        request.session['auth_id'] = user.id
        request.session['auth_name'] = user.first_name
        return RedirectResponse(url="/admin/dashboard", status_code=302)

@router.get('/forgot-password', response_class=HTMLResponse, name='admin.forgot-password.form')
async def forgot_password(request: Request):
    return templates.TemplateResponse('auth/forgot-password.html', {'request': request})

@router.post('/forgot-password', response_class=HTMLResponse, name='admin.forgot-password.store')
async def forgot_password_store(request: Request, email: str = Form()):
    if auth_service.reset_password(email, request) :
        return templates.TemplateResponse('auth/forgot-password.html', {
            'request': request,
            'error_msg': "Please check your inbox, we have sent you reset password email.",
            'error_class': 'alert-success'
        })
    else:
        return templates.TemplateResponse('auth/forgot-password.html', {
            'request': request,
            'error_msg': "We can't find user with provided email."
        })


@router.get('/reset-password/{token}', response_class=HTMLResponse, name='admin.reset-password.form')
async def reset_password(token: str, request: Request, service: UserTokenService = Depends(get_user_token_service)):
    user_token = service.getResetPasswordToken(token=token)
    return templates.TemplateResponse('auth/reset-password.html', {"request": request, 'user_token': user_token})

@router.post('/reset-password', name='admin.reset-password.store')
async def reset_password_store(request: Request,
                               token: str = Form(...),
                               password: str = Form(...),
                               password_confirm: str = Form(...),
                               service: UserTokenService = Depends(get_user_token_service),
                               user_service: UserService = Depends(get_user_tservice),
                               ):
    user_token = service.getResetPasswordToken(token=token)
    try:
        data = ResetPasswordSchema(
            password=password,
            password_confirm=password_confirm
        )
        user_service.update_password(user_token.user_id, data.password)
        service.delete(user_token.id)
        return RedirectResponse(url="/admin/login", status_code=302)
    except ValidationError as e:
        return templates.TemplateResponse('auth/reset-password.html', {
            "request": request,
            "user_token": user_token,
            "error_msg": str(e)
        })

