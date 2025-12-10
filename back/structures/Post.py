from pydantic import BaseModel
from structures.User import User

class Post(BaseModel):
    title: str
    content: str
    author: User
    children: list[Post]

