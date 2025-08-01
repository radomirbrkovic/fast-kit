from models.user import Users
from repositories.admin.crud_repository import CrudRepository
from sqlalchemy.orm import Session

class UserRepository(CrudRepository):
    def __init__(self, db: Session):
        super().__init__(db, Users)