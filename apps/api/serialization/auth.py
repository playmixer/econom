from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str


class Source(BaseModel):
    isAuth: bool
    model: Optional[User]
