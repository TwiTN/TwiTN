import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    title = db.Column(
        String(50),
        nullable=False,
    )

    content = db.Column(
        String(500),
        nullable=False,
    )

    author_username = db.Column(
        String(20),
        ForeignKey("users.username"),
        nullable=False,
        index=True,
    )

    response_to = db.Column(
        UUID(as_uuid=True),
        ForeignKey("posts.id"),
        nullable=True,
    )

    author = relationship(
        "User",
        backref="posts",
        lazy=True,
    )

    parent = relationship(
        "Post",
        remote_side=[id],
        backref="replies",
        lazy=True,
    )

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content,
            "author": self.author.to_dict() if self.author else None,
            "response_to": str(self.response_to) if self.response_to else None,
        }
