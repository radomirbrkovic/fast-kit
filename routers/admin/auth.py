from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from routers.admin.admin import router, templates


@router.get('/login', response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse('sign-in.html', {"request": request})

@router.post('/login', response_class=HTMLResponse)
async def authenticate(request: Request, email: str = Form(), password: str= Form()):
    return templates.TemplateResponse('sign-in.html', {"request": request, 'error_msg': "Invalid credentials."})