from db.model.User import User
from db import db
from sqlalchemy.exc import IntegrityError


def get_user(username: str) -> User | None:
    return db.session.get(User, username)


def add_user(username, display_name, email, password):
    user = User(
        username=username, display_name=display_name, email=email, password=password
    )

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None
    db.session.refresh(user)
    return user


def delete_user(username: str):
    user = db.session.get(User, username)
    db.session.delete(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Exception("Can't delete user")
    db.session.refresh(user)
    return user
