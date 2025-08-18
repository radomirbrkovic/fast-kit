from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PageCreate(BaseModel):
    title: str
    content: Optional[str] = None
    published_at: Optional[date] = None
    slug: str | None = Field(default=None, exclude=True)

class PageUpdate(BaseModel):
    title: str
    content: Optional[str] = None
    published_at: Optional[date] = None
    slug: str | None = Field(default=None, exclude=True)

class PageOut(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    published_at: date