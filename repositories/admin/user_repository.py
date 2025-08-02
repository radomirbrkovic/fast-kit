from models.user import Users
from repositories.admin.crud_repository import CrudRepository
from sqlalchemy.orm import Session
from sqlalchemy import or_

class UserRepository(CrudRepository):
    def __init__(self, db: Session):
        super().__init__(db, Users)

    def get(self, filters: dict = None):
        users = self.db.query(self.model)

        if filters is not None and 'query' in filters and filters['query'] != '':
            like_term = f"%{filters['query']}%"
            users = users.filter(
                or_(
                    self.model.first_name.ilike(like_term),
                    self.model.last_name.ilike(like_term),
                    self.model.email.ilike(like_term),
                    self.model.phone_number.ilike(like_term),
                )
            )

        if filters is not None and 'page' in filters and filters['page'] > 0:
            users = users.limit(self.ITEMS_PER_PAGE).offset(self.ITEMS_PER_PAGE * filters['page'])

        return users.all()