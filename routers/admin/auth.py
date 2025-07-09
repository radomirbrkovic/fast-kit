from routers.admin.admin import router

@router.get('/login')
async def login_form():
    return {"Login form"}