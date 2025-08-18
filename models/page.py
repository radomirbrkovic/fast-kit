from sqlalchemy import Column, Integer, String, DateTime, Text
from infastructure.database import Base

class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    slug = Column(String, unique=True, index=True)
    content = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True, index=True)