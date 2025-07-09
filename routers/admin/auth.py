from fastapi import Request
from fastapi.responses import HTMLResponse
from routers.admin.admin import router, templates


@router.get('/login', response_class=HTMLResponse)
async def sing_in(request: Request):
    return templates.TemplateResponse('sign-in.html', {"request": request})