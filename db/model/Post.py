import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import db
import structures


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

    author = db.Column(
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

    posted_at = db.Column(
        db.DateTime,
        nullable=False,
    )

    parent = relationship(
        "Post",
        remote_side=[id],
        backref="replies",
        lazy=True,
    )

    def to_structure(self, depth=0) -> "structures.Post":
        return structures.Post(
            id=str(self.id),
            title=self.title,
            content=self.body,
            author=self.author_fk.to_structure() if self.author_fk else None,
            response_to=str(self.reply_to) if self.reply_to else None,
            replies=[reply.to_structure(depth=depth - 1) for reply in self.replies]
            if depth > 0
            else [],
        )
