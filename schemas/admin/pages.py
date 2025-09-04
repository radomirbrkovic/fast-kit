from pydantic import BaseModel, BeforeValidator
from typing import Optional, Annotated, Union
from datetime import datetime, date

def parse_date(value):
    if value in (None, "", "null"):  # ✅ skip empty
        return None
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%m/%d/%Y").date()
        except ValueError:
            raise ValueError("Date must be in MM/DD/YYYY format")
    return value

class PageCreate(BaseModel):
    title: str
    content: Optional[str] = None
    published_at: Optional[Annotated[Union[date, None], BeforeValidator(parse_date)]] = None
    slug: Optional[str] = None

class PageUpdate(BaseModel):
    title: str
    content: Optional[str] = None
    published_at: Optional[Annotated[Union[date, None], BeforeValidator(parse_date)]] = None
    slug: Optional[str] = None

class PageOut(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    published_at: date