from sqlalchemy import String
from db import db
import structures


class User(db.Model):
    __tablename__ = "users"

    username: str = db.Column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
        primary_key=True,
    )

    display_name: str = db.Column(
        String(50),
        nullable=False,
    )

    email: str = db.Column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    password: str = db.Column(
        String(128),
        nullable=False,
    )

    posts = db.relationship(
        "Post",
        cascade="delete-orphan, all",
        backref="author_fk",
    )

    def to_structure(self) -> "structures.User":
        from structures import User as UserStructure

        return UserStructure(
            username=self.username,
            display_name=self.display_name,
            email=self.email,
        )
