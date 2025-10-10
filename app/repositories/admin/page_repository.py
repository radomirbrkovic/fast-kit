from app.repositories.admin.crud_repository import CrudRepository
from sqlalchemy.orm import Session
from app.models.page import Page

class PageRepository(CrudRepository):
    def __init__(self, db: Session):
        super().__init__(db, Page)

    def is_slug_exists(self, slug: str):
        return self.db.query(self.model).filter(Page.slug == slug).first()