from schemas.admin.pages import PageCreate, PageUpdate
from repositories.admin.page_repository import PageRepository
from services.admin.base_crud_service import BaseCrudService, CreateSchemaType, ModelType
from models.page import Page
from slugify import slugify

class PageService(BaseCrudService[Page, PageCreate, PageUpdate]):
    def __init__(self, repo: PageRepository):
        super().__init__(repo)

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in.slug = self._get_slug(obj_in.title)
        return self.repository.create(obj_in)

    def update(self, id: int, obj_in: CreateSchemaType) -> ModelType:
        obj_in.slug = self._get_slug(obj_in.title)
        return super().update(id, obj_in)

    def _get_slug(self, title: str) -> str:
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while self.repository.is_slug_exists(slug):
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug