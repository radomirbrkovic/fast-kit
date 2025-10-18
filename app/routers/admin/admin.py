from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from app.middlewares.admin_middleware import auth
from app.infrastructure.database.connection import get_database_connection
from app.infrastructure.tranaslations import TranslationManager

public_router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    include_in_schema= False
)

guard_router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    include_in_schema= False,
    dependencies=[Depends(auth)]
)

templates = Jinja2Templates(directory='templates/admin')

translation_manager = TranslationManager()
templates.env.globals['gettext'] = translation_manager.gettext
db_connection = get_database_connection()

def get_db():
    db = db_connection.get_session()
    try:
        yield db
    finally:
        db.close()