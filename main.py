from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import os
from app.routers.admin.auth import router as admin_auth_router
from app.routers.admin.dashboard import router as admin_dashboard_router
from app.routers.admin.users import router as admin_users_router
from app.routers.admin.pages import router as admin_pages_router
from app.middlewares.admin_middleware import GlobalContextMiddleware
from app.infrastructure.tranaslations import TranslationManager

#API routers
from app.routers.api.auth import router as api_auth_router

app = FastAPI()

app.add_middleware(SessionMiddleware, os.getenv('ADMIN_SECRET_KEY', ''))
app.add_middleware(GlobalContextMiddleware)
app.include_router(admin_auth_router)
app.include_router(admin_dashboard_router)
app.include_router(admin_users_router)
app.include_router(admin_pages_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

translation_manager = TranslationManager()

#API routers
app.include_router(api_auth_router)

@app.get('/')
async def welcome():
    return {"message": translation_manager.gettext('welcome_message')}