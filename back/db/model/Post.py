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

    body = db.Column(
        String(500),
        nullable=False,
    )

    author_username = db.Column(
        String(20),
        ForeignKey("users.username"),
        nullable=False,
        index=True,
    )

    reply_to = db.Column(
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

    # ✅ requis par les tests
    @classmethod
    def create(
        cls,
        title: str,
        content: str,
        author_username: str,
        response_to=None,
    ):
        post = cls(
            title=title,
            body=content,
            author_username=author_username,
            reply_to=response_to,
        )
        db.session.add(post)
        db.session.commit()
        return post

    # ✅ format attendu par l'API + tests
    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.body,
            "author": self.author.to_dict() if self.author else None,
            "response_to": str(self.reply_to) if self.reply_to else None,
        }
