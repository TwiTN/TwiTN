from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import db


class Reaction(db.Model):
    __tablename__ = "reaction"

    post = db.Column(
        UUID(as_uuid=True),
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        primary_key=True,
    )

    author = db.Column(
        String(20),
        ForeignKey("users.username", ondelete="CASCADE"),
        nullable=False,
        index=True,
        primary_key=True,
    )

    character = db.Column(
        String(1),
        nullable=False,
        index=True,
        primary_key=True,
    )

    post_rel = relationship(
        "Post",
        backref="reactions",
        lazy=True,
    )

    user = relationship(
        "User",
        backref="reactions",
        lazy=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "post",
            "author",
            "character",
        ),
    )
