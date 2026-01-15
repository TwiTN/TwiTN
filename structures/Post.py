from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, RootModel, Field

from structures.User import User
from lib import UUID_RE
from db.api.Reaction import get_reactions_summary


class Post(BaseModel):
    id: str = Field(
        ...,
        description="Post ID",
        example=str(uuid.uuid4()),
        format="uuid",
        pattern=UUID_RE,
    )

    title: str = Field(
        ...,
        description="Title of the post",
        max_length=50,
    )

    content: str = Field(
        ...,
        description="Content of the post",
        max_length=500,
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp of the post",
        example="2024-01-01T12:00:00Z",
    )

    author: User = Field(
        ...,
        description="Author of the post",
    )

    response_to: Optional[str] = Field(
        None,
        description="ID of the post this is responding to",
        example=str(uuid.uuid4()),
        format="uuid",
        pattern=UUID_RE,
    )

    replies: List["Post"] = Field(
        default_factory=list,
        description="List of replies to this post",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author.to_dict(),
            "response_to": self.response_to,
            "replies": [reply.to_dict() for reply in self.replies],
            "reactions": get_reactions_summary(self.id),
        }


class PostSubmit(BaseModel):
    title: str = Field(
        ...,
        description="Title of the post",
        max_length=50,
    )
    body: str = Field(
        ...,
        description="Content of the post",
        max_length=500,
    )
    reply_to: Optional[str] = Field(
        None,
        description="ID of the post this is responding to",
        example=str(uuid.uuid4()),
        format="uuid",
        pattern=UUID_RE,
    )


class PostUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        description="Title of the post",
        max_length=50,
    )
    content: Optional[str] = Field(
        None,
        description="Content of the post",
        max_length=500,
    )


class PostList(RootModel):
    root: List[Post] = Field(
        ...,
        description="List of posts",
    )

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def to_array(self):
        return [post.to_dict() for post in self.root]


class PostId(BaseModel):
    post_id: uuid.UUID = Field(
        ...,
        description="Post ID",
    )

class PostIdWithReaction(PostId):
    reaction: str = Field(
        ...,
        description="Reaction type",
        max_length=1,
        min_length=1,
        example="👍",
    )
