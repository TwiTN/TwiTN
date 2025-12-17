from sqlalchemy import String
from db import db


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(
        String(20),
        unique=True,
        index=True,
        nullable=False,
        primary_key=True
    )

    display_name = db.Column(
        String(50),
        nullable=False,
    )

    email = db.Column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    password = db.Column(
        String(128),
        nullable=False,
    )

    def to_dict(self):
        return {
            "username": self.username,
            "display_name": self.display_name,
            "email": self.email,
        }
