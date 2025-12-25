import uuid
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import db
import structures


class Reaction(db.Model):
    __tablename__ = "reactions"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    post_id = db.Column(
        UUID(as_uuid=True),
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    username = db.Column(
        String(20),
        ForeignKey("users.username", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    reaction = db.Column(
        String(1),
        nullable=False,
        index=True,
    )

    post = relationship(
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
            "post_id",
            "username",
            name="uq_reaction_post_user",
        ),
    )

    def to_structure(self) -> "structures.Reaction":
        from structures import Reaction as ReactionStructure

        return ReactionStructure(
            id=str(self.id),
            post_id=str(self.post_id),
            username=self.username,
            reaction=self.reaction,
        )
