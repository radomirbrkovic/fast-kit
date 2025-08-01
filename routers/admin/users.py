from fastapi import Request
from fastapi.responses import HTMLResponse
from routers.admin.admin import guard_router, templates

router = guard_router

@router.get('/users', response_class=HTMLResponse, name="admin.users.index")
async def index(request: Request):
    query = request.query_params.get("q", "")
    return templates.TemplateResponse('users/index.html', {'request': request, 'query': query})