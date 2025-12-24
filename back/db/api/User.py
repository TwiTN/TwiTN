from db.model.User import User
from db import db
from sqlalchemy.exc import IntegrityError


def get_user(username: str) -> User | None:
    return db.session.query(User).filter(User.username == username).first()


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
    user = get_user(username)

    if not user:
        return None
    user = db.session.merge(user)

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Can't delete user: {e}")
    return True
