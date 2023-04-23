from sqlalchemy import Column, Integer

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)

    def __str__(self) -> str:
        return f"User:{self.user_id}"
