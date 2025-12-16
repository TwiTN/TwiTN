from flask_openapi3 import APIBlueprint
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
def get_user() -> User:
    raise NotImplementedError("User retrieval not implemented yet.")


@api.patch(
    "/",
    tags=[user_tag],
    responses={200: User},
    summary="Update current user information",
    description="Update information about the currently authenticated user.",
)
def update_user(body: UserPatch) -> User:
    raise NotImplementedError("User update not implemented yet.")


@api.delete(
    "/",
    tags=[user_tag],
    responses={204: None},
    summary="Delete current user",
    description="Delete the currently authenticated user and removes the cookie.",
)
def delete_user() -> None:
    raise NotImplementedError("User deletion not implemented yet.")


@api.get(
    "/<string:username>",
    tags=[user_tag],
    responses={200: User},
    summary="Get user information by username",
    description="Retrieve information about a user by their username.",
)
def get_user_by_id(
    path: UserId,
) -> User:
    raise NotImplementedError("User retrieval by ID not implemented yet.")


@api.post(
    "/",
    tags=[user_tag],
    responses={201: User},
    summary="Create a new user",
    description="Create a new user account.",
)
def create_user(body: UserSignUp) -> User:
    raise NotImplementedError("User creation not implemented yet.")


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
