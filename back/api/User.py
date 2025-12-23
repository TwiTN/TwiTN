from flask_openapi3 import APIBlueprint
from flask import request, abort
from back.structures import User, UserSignUp, UserLogin, UserId
from .tags import user_tag
from flask import abort
from back.db import get_user, add_user, delete_user
from back.db.model.User import User as DBUser
from flask import make_response

import back.lib.session as session


api = APIBlueprint("User", __name__, url_prefix="/user")


# =========================
# GET CURRENT USER
# =========================
@api.get(
    "/",
    tags=[user_tag],
    responses={200: User},
    summary="Get current user information",
    description="Retrieve information about the currently authenticated user.",
)
def get_current_user() -> User:
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(401, description="Not authenticated")

    username = session.get_user_from_session(session_id)
    if not username:
        abort(401, description="Invalid session")

    user = get_user(username)
    if user is None:
        abort(404, description="User not found")

    return user


# =========================
# GET USER BY ID
# =========================
@api.get(
    "/<string:username>",
    tags=[user_tag],
    responses={200: User},
)
def get_user_by_id(path: UserId) -> User | None:
    user = get_user(path.username)
    if user is None:
        return None, 404
    return user, 200


# =========================
# DELETE USER
# =========================
@api.delete(
    "/<string:username>",
    tags=[user_tag],
    responses={204: None},
)
def del_user(path: UserId) -> None:
    delete_user(path.username)
    return None, 204


# =========================
# CREATE USER
# =========================
@api.post(
    "/",
    tags=[user_tag],
    responses={201: User},
    summary="Create a new user",
    description="Create a new user account.",
)
def create_user(body: UserSignUp):
    user = add_user(
        body.username,
        body.display_name,
        body.email,
        body.password,
    )

    if user is None:
        return make_response(
            {"error": "User already exists"},
            409,
        )

    # ✅ convertir le modèle Pydantic en dict
    return make_response(user.to_dict(), 201)



# =========================
# LOGIN
# =========================
@api.post(
    "/login",
    tags=[user_tag],
    responses={200: User},
    summary="User login",
    description="Authenticate a user and create a session.",
)
def login_user(body: UserLogin) -> User:
    db_user = DBUser.query.filter_by(username=body.username).first()
    if not db_user:
        abort(401, description="Invalid username or password")

    if db_user.password != body.password:
        abort(401, description="Invalid username or password")

    session_id = session.create_session(db_user.username)

    user = get_user(db_user.username)
    response = api.make_response(user)

    response.set_cookie(
        "session_id",
        session_id,
        httponly=True,
        samesite="Lax",
    )

    return response


# =========================
# LOGOUT
# =========================
@api.get(
    "/logout",
    responses={200: None},
    tags=[user_tag],
    summary="User logout",
    description="Logout the currently authenticated user and destroy the session.",
)
def logout_user():
    session_id = request.cookies.get("session_id")
    if session_id:
        session.delete_session(session_id)

    response = api.make_response("")
    response.delete_cookie("session_id")
    return response
