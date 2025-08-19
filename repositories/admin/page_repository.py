from repositories.admin.crud_repository import CrudRepository
from sqlalchemy.orm import Session
from models.page import Page

class UserRepository(CrudRepository):
    def __init__(self, db: Session):
        super().__init__(db, Page)