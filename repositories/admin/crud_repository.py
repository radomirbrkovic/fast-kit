from sqlalchemy.orm import Session
from .base import AbstractRepository

class CrudRepository(AbstractRepository):

    ITEMS_PER_PAGE = 20

    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def find(self, id: int):
        return self.db.query(self.model).get(id)

    def get(self, filters: dict = None):
        items = self.db.query(self.model)
        if filters is not None and 'page' in filters and filters['page'] > 0:
            items = items.limit(self.ITEMS_PER_PAGE).offset(self.ITEMS_PER_PAGE * filters['page'])
        return items.all()

    def create(self, obj_in):
        db_obj = self.model(**obj_in.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, id: int, obj_in):
        db_obj = self.find(id)
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int):
        db_obj = self.find(id)
        self.db.delete(db_obj)
        self.db.commit()