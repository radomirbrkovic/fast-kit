from fastapi import Request
from fastapi.responses import HTMLResponse
from app.routers.admin.admin import guard_router, templates

router = guard_router

@router.get('/dashboard', response_class=HTMLResponse, name='admin.dashboard')
async def dashboard(request: Request):
    return templates.TemplateResponse('dashboard.html', {'request': request})