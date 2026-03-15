from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class BookCreate(BaseModel):
    title: str
    author: str
    category: str
    cover: str