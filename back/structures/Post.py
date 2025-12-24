from __future__ import annotations
import uuid
from pydantic import BaseModel, RootModel, Field
from structures.User import User
from typing import List, Optional
from lib import UUID_RE


class Post(BaseModel):
    id: str = Field(
        ...,
        description="Post ID",
        example=str(uuid.uuid4()),
        format="uuid",
        pattern=UUID_RE,
    )
    title: str = Field(..., description="Title of the post", max_length=50)
    content: str = Field(..., description="Content of the post", max_length=500)
    author: User = Field(..., description="Author of the post")
    response_to: Optional[str] = Field(
        ...,
        description="ID of the post this is responding to",
        example=str(uuid.uuid4()),
        format="uuid",
        pattern=UUID_RE,
    )
    replies: List[Post] = Field(
        default_factory=list, description="List of replies to this post"
    )


class PostSubmit(BaseModel):
    title: str = Field(..., description="Title of the post", max_length=50)
    content: str = Field(..., description="Content of the post", max_length=500)
    response_to: Optional[str] = Field(
        None,
        description="ID of the post this is responding to",
        example=str(uuid.uuid4()),
        format="uuid",
        pattern=UUID_RE,
    )


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title of the post", max_length=50)
    content: Optional[str] = Field(
        None, description="Content of the post", max_length=500
    )


class PostList(RootModel):
    root: List[Post] = Field(..., description="List of posts")

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


class PostId(BaseModel):
    post_id: uuid.UUID = Field(..., description="Post ID")


class PostIdWithReaction(BaseModel):
    post_id: uuid.UUID = Field(..., description="Post ID")
    reaction: str = Field(
        ..., description="Reaction type", max_length=1, min_length=1, example="👍"
    )
