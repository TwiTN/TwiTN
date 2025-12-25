from flask_openapi3 import APIBlueprint
from flask import session
from db.api import get_user, add_user, delete_user
from lib.make_error import make_error
from structures import User, UserSignUp, UserLogin, UserId
from .tags import user_tag

api = APIBlueprint("User", __name__, url_prefix="user")


@api.get(
    "/",
    tags=[user_tag],
    responses={200: User},
    summary="Get current user",
)
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return make_error(401, "Unauthorized")

    user = get_user(user_id)
    if user is None:
        return make_error(404, "User not found")

    return user.to_structure().to_dict()


@api.get(
    "/<string:username>",
    tags=[user_tag],
    responses={200: User},
)
def get_user_by_id(path: UserId):
    user = get_user(path.username)
    if user is None:
        return make_error(404, "User not found")

    return user.to_structure().to_dict()


@api.post(
    "/",
    tags=[user_tag],
    responses={201: User},
)
def create_user(body: UserSignUp):
    user = add_user(
        body.username,
        body.display_name,
        body.email,
        body.password,
    )

    if user is None:
        return make_error(409, "User already exists")

    return user.to_structure().to_dict(), 201


@api.post(
    "/login",
    tags=[user_tag],
    responses={200: User},
)
def login_user(body: UserLogin):
    user = get_user(body.username)
    if user is None or user.password != body.password:
        return make_error(401, "Invalid credentials")

    session["user_id"] = body.username

    return user.to_structure().to_dict()


@api.post("/logout", tags=[user_tag], responses={200: None})
def logout_user():
    session.pop("user_id", None)

    return make_error(200, "Logged out")


@api.delete(
    "/",
    tags=[user_tag],
    responses={204: None},
)
def delete_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return make_error(401, "Unauthorized")

    deleted = delete_user(user_id)
    if not deleted:
        return make_error(404, "User not found")

    session.pop("user_id", None)
    return make_error(204, "User deleted")
