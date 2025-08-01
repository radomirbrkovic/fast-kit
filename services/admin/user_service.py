from schemas.admin.users import UserCreate, UserUpdate
from services.admin.base_crud_service import BaseCrudService
from repositories.admin.user_repository import UserRepository
from models.user import Users

class UserService(BaseCrudService[Users, UserCreate, UserUpdate]):
    def __init__(self, repo: UserRepository):
        super().__init__(repo)