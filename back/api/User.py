from flask_openapi3 import APIBlueprint, APIBlueprint
from db import get_user, add_user, delete_user
from structures import User, UserSignUp, UserPatch, UserLogin, UserId
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
    raise NotImplementedError("User retrieval not implemented yet.")

@api.get(
    "/<string:uuid>",
    tags=[user_tag],
    responses={200: User},
)
def get_user_by_id(path: UserId) -> User | None:
    user = get_user(path.username)
    if user == None:
        return None, 404
    return user,200

@api.delete("/<uuid>",
        tags=[user_tag],
        responses={204: None}
)
def del_user(path: UserId) -> None:
    delete_user(path.username)

@api.post(
    "/",
    tags=[user_tag],
    responses={201: User},
    summary="Create a new user",
    description="Create a new user account.",
)
def create_user(
    body: UserSignUp
) -> User | None:
    user = add_user(body.username,body.display_name,body.email,body.password)
    if user==None:
        return None, 409
    return user, 201


@api.post(
    "/login",
    tags=[user_tag],
    responses={200: User},
    summary="User login",
    description="Authenticate a user and create a session.",
)
def login_user(body: UserLogin) -> User:
    raise NotImplementedError("User login not implemented yet.")


@api.get(
    "/logout",
    responses={200: None},
    tags=[user_tag],
    summary="User logout",
    description="Logout the currently authenticated user and destroy the session.",
)
def logout_user():
    raise NotImplementedError("User logout not implemented yet.")
