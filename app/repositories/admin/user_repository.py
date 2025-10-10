from app.models.user import Users
from app.repositories.admin.crud_repository import CrudRepository
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.schemas.admin.users import UserCreate

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

        users = self.paginate(users, filters)

        return users.all()

    def create(self, obj_in: UserCreate):
        user_dict = obj_in.model_dump(exclude={"password"})
        db_obj = self.model(**user_dict)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update_password(self, id: int, password: str):
        db_obj = self.db.query(Users).filter(Users.id == id).first()
        db_obj.hashed_password=password
        self.db.commit()
        self.db.refresh(db_obj)