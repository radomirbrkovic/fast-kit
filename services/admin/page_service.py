from schemas.admin.pages import PageCreate, PageUpdate
from repositories.admin.page_repository import PageRepository
from services.admin.base_crud_service import BaseCrudService
from models.page import Page

class PageService(BaseCrudService[Page, PageCreate, PageUpdate]):
    def __init__(self, repo: PageRepository):
        super().__init__(repo)
