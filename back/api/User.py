from flask_openapi3 import APIBlueprint
from flask import session
from db import get_user, add_user, delete_user
from lib.make_error import make_error
from structures import User, UserSignUp, UserLogin, UserId
from .tags import user_tag

api = APIBlueprint("User", __name__, url_prefix="/user")


@api.get(
    "/",
    tags=[user_tag],
    responses={200: User},
    summary="Get current user information",
    description="Retrieve information about the currently authenticated user.",
)
def get_current_user() -> User:
    user_id = session.get("user_id")
    if not user_id:
        return make_error(401, "Unauthorized: No user logged in")
    user = get_user(user_id)
    if user is None:
        return make_error(404, "User not found")
    return user.to_dict(), 200


@api.get(
    "/<string:username>",
    tags=[user_tag],
    responses={200: User},
)
def get_user_by_id(path: UserId) -> User | None:
    user = get_user(path.username)
    if user is None:
        return make_error(404, "User not found")
    return user.to_dict(), 200


@api.delete("/", tags=[user_tag], responses={204: None})
def delete_current_user() -> None:
    user_id = session.get("user_id")
    if not user_id:
        return make_error(401, "Unauthorized: No user logged in")
    delete_user(user_id)
    session.pop("user_id", None)
    return {}, 204

@api.post(
    "/",
    tags=[user_tag],
    responses={201: User},
    summary="Create a new user",
    description="Create a new user account.",
)
def create_user(body: UserSignUp) -> User | None:
    user = add_user(body.username, body.display_name, body.email, body.password)
    if user is None:
        return make_error(409, "User already exists")
    return user.to_dict(), 201


@api.post(
    "/login",
    tags=[user_tag],
    responses={200: User},
    summary="User login",
    description="Authenticate a user and create a session.",
)
def login_user(body: UserLogin) -> dict:
    user = get_user(body.username)
    if user is None or user.password != body.password:
        return make_error(401, "Invalid username or password")
    session["user_id"] = user.username
    
    return user.to_dict(), 200


@api.get(
    "/logout",
    responses={200: None},
    tags=[user_tag],
    summary="User logout",
    description="Logout the currently authenticated user and destroy the session.",
)
def logout_user():
    session.pop("user_id", None)
    return make_error(200, "Successfully logged out")

