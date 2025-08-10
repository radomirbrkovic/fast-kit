from sqlalchemy.orm import Session
from models.user_token import  UserToken
from models.enums import UserTokenType

class UserTokenRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = UserToken

    def create(self, data: dict):
        db_obj = self.model(**data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def find(self, id: int):
        return self.db.query(self.model).get(id)

    def findByTokenAndType(self, token: str, token_type: UserTokenType):
        return self.db.query(self.model).filter(UserToken.token == token, UserToken.type == token_type).first()

    def delete(self, id: int):
        db_obj = self.find(id)
        self.db.delete(db_obj)
        self.db.commit()
