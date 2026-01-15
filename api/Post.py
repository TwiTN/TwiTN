from lib.make_error import make_error
from flask_openapi3 import APIBlueprint
from structures import Post, PostList, PostSubmit, Paging, PostId, Depth
from .Reactions import api as reactions_api
from .tags import post_tag
import datetime
import time
from db.api import (
    list_posts,
    get_post,
    create_post as create_post_service,
    delete_post as delete_post_service,
)
from flask import session
from db.api.User import get_user


api = APIBlueprint("Post", __name__, url_prefix="/posts")
api.register_api(reactions_api)


@api.get(
    "/",
    tags=[post_tag],
    responses={200: PostList},
    summary="Get a list of posts",
)
def get_posts(query: Paging) -> PostList:
    posts = list_posts(
        limit=getattr(query, "limit", 20),
        offset=getattr(query, "offset", 0),
    )

    return PostList([post.to_structure() for post in posts]).to_array()


@api.get(
    "/<uuid:post_id>",
    tags=[post_tag],
    responses={200: Post},
    summary="Get post by ID",
)
def get_post_by_id(path: PostId, query: Depth) -> Post:
    post = get_post(path.post_id)

    if post is None:
        return make_error(404, "Post not found")

    return post.to_structure(depth=query.depth).to_dict()

@api.post(
    "/",
    tags=[post_tag],
    responses={201: Post},
    summary="Create a new post",
)
def create_post(body: PostSubmit) -> Post:
    if "user_id" not in session:
        return make_error(401, "Authentication required")

    user = get_user(session["user_id"])
    if user is None:
        return make_error(404, "User not found")

    post = create_post_service(
        title=body.title,
        body=body.body,
        author=user.username,
        reply_to=body.reply_to,
        posted_at=datetime.datetime.fromtimestamp(time.time(), datetime.timezone.utc),
    )

    return post.to_structure().to_dict(), 201


@api.delete(
    "/<uuid:post_id>",
    tags=[post_tag],
    responses={204: None},
    summary="Delete a post",
)
def delete_post(path: PostId) -> None:
    if "user_id" not in session:
        return make_error(401, "Authentication required")

    user = get_user(session["user_id"])
    if user is None:
        return make_error(404, "User not found")

    post = get_post(path.post_id)
    if post is None:
        return make_error(404, "Post not found")

    if post.author != user.username:
        return make_error(403, "You are not allowed to delete this post")

    delete_post_service(path.post_id)
    return make_error(204, "Post deleted")
