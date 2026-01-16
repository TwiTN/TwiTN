from sqlite3 import IntegrityError
from flask_openapi3 import APIBlueprint
from flask import session
from db.model import User, Post
from lib.responses import make_error, make_success
import structures
from .tags import user_tag

api = APIBlueprint("User", __name__, url_prefix="user")


@api.get(
    "/",
    tags=[user_tag],
    responses={200: structures.User},
    summary="Get current user",
)
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return make_error(401, "Unauthorized")

    user: User = User.query.get(user_id)
    if user is None:
        return make_error(404, "User not found")

    return user.to_structure().to_dict()


@api.get(
    "/<string:username>",
    tags=[user_tag],
    responses={200: structures.User},
    summary="Get the specified user"
)
def get_user(path: structures.UserId):
    user: User = User.query.get(path.username)
    if user is None:
        return make_error(404, "User not found")

    return user.to_structure().to_dict()


@api.get(
    "/<string:username>/posts",
    tags=[user_tag],
    responses={200: structures.PostList},
    summary="Get posts by user",
)
def get_user_posts(path: structures.UserId, query: structures.Paging):
    user: User = User.query.get(path.username)
    if user is None:
        return make_error(404, "User not found")

    posts: list[Post] = (
        Post.query.filter_by(author=path.username)
        .order_by(Post.posted_at.desc())
        .limit(query.size)
        .offset(query.page * query.size)
        .all()
    )

    return structures.PostList([post.to_structure() for post in posts]).to_array()


@api.post(
    "/",
    tags=[user_tag],
    responses={201: structures.User},
    summary="Register a new user"
)
def create_user(body: structures.UserSignUp):
    user = User(
        username=body.username, display_name=body.display_name, email=body.email
    )
    user.update_password(body.password)

    try:
        User.query.session.add(user)
        User.query.session.commit()
    except IntegrityError:
        User.query.session.rollback()
        if user is None:
            return make_error(409, "User already exists")
    User.query.session.refresh(user)
    return user.to_structure().to_dict(), 201


@api.post(
    "/login",
    tags=[user_tag],
    responses={200: structures.User},
    summary="Authenticate the user using username and password"
)
def login_user(body: structures.UserLogin):
    user: User = User.query.get(body.username)
    if user is None or not user.verify_password(body.password):
        return make_error(401, "Invalid credentials")

    session["user_id"] = body.username

    return user.to_structure().to_dict()


@api.post("/logout", tags=[user_tag], responses={200: None},summary="Logout the user")
def logout_user():
    session.pop("user_id", None)

    return make_success(200, "Logged out")


@api.delete(
    "/",
    tags=[user_tag],
    responses={204: None},
    summary="Delete the current user"
)
def delete_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return make_error(401, "Unauthorized")

    user = User.query.get(user_id)
    if not user:
        return make_error(404, "User not found")

    User.query.session.delete(user)
    User.query.session.commit()
    session.pop("user_id", None)

    return make_success(204, "User deleted")
