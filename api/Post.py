from lib.responses import make_error, make_success
from flask_openapi3 import APIBlueprint
from .Reactions import api as reactions_api
from .tags import post_tag
import datetime
import time
from flask import session
from db.model import User, Post
import structures


api = APIBlueprint("Post", __name__, url_prefix="/posts")
api.register_api(reactions_api)


@api.get(
    "/",
    tags=[post_tag],
    responses={200: structures.PostList},
    summary="Get a list of posts",
)
def get_posts(query: structures.Paging) -> structures.PostList:
    start = query.page * query.size
    limit = query.size

    posts: list[Post] = (
        Post.query.order_by(Post.posted_at.desc())
        .filter_by(reply_to=None)
        .limit(limit)
        .offset(start)
        .all()
    )

    return structures.PostList([post.to_structure() for post in posts]).to_array()


@api.get(
    "/<uuid:post_id>",
    tags=[post_tag],
    responses={200: structures.Post},
    summary="Get post by ID",
)
def get_post_by_id(path: structures.PostId, query: structures.Depth) -> structures.Post:
    post: Post = Post.query.get(path.post_id)

    if post is None:
        return make_error(404, "Post not found")

    return post.to_structure(depth=query.depth).to_dict()


@api.post(
    "/",
    tags=[post_tag],
    responses={201: structures.Post},
    summary="Create a new post",
)
def create_post(body: structures.PostSubmit) -> structures.Post:
    if "user_id" not in session:
        return make_error(401, "Authentication required")

    user: User = User.query.get(session["user_id"])
    if user is None:
        return make_error(404, "User not found")

    post: Post = Post(
        title=body.title,
        body=body.body,
        author=user.username,
        reply_to=body.reply_to,
        posted_at=datetime.datetime.fromtimestamp(time.time(), datetime.timezone.utc),
    )

    Post.query.session.add(post)
    Post.query.session.commit()

    return post.to_structure().to_dict(), 201


@api.delete(
    "/<uuid:post_id>",
    tags=[post_tag],
    responses={204: None},
    summary="Delete a post",
)
def delete_post(path: structures.PostId) -> None:
    if "user_id" not in session:
        return make_error(401, "Authentication required")

    user: User = User.query.get(session["user_id"])
    if user is None:
        return make_error(404, "User not found")

    post: Post = Post.query.get(path.post_id)
    if post is None:
        return make_error(404, "Post not found")

    if post.author != user.username:
        return make_error(403, "You are not allowed to delete this post")

    Post.query.session.delete(post)
    Post.query.session.commit()

    return make_success(204, "Post deleted")
