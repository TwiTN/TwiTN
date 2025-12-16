from pydantic import BaseModel, RootModel
from structures.User import User
from typing import List, Optional

class Post(BaseModel):
    title: str
    content: str
    author: User
    response_to: Optional[str] = None 
    replies: List[Post] = []

class PostSubmit(BaseModel):
    title: str
    content: str
    response_to: Optional[str] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostList(RootModel):
    root: List[Post]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
    
class GetPostQuery(BaseModel):
    depth: int = 0
