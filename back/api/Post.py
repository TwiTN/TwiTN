from flask_openapi3 import APIBlueprint
from structures import Post, PostList, PostSubmit, DepthPaging, Paging, PostId
from .Reactions import api as reactions_api
from .tags import post_tag
from db.services.post import list_posts
from db.services.post import get_post
from db.services.post import create_post as create_post_service
from db.services.post import delete_post as delete_post_service
from flask import session
from db.api.User import get_user


api = APIBlueprint("Post", __name__, url_prefix="/posts")
api.register_api(reactions_api)


@api.get("/", tags=[post_tag], responses={200: PostList}, summary="Get a list of posts")
def get_posts(
    query: Paging,
) -> PostList:
    posts = list_posts(
        limit=query.limit,
        offset=query.offset,
    )

    return PostList([post.to_dict() for post in posts])


@api.get(
    "/<uuid:post_id>", tags=[post_tag], responses={200: Post}, summary="Get post by ID"
)
def get_post_by_id(path: PostId, query: DepthPaging) -> Post:
    post = get_post(path.post_id)

    if post is None:
        return None  # flask_openapi3 gère le 404

    return post.to_dict()


@api.post(
    "/",
    tags=[post_tag],
    responses={201: Post},
    summary="Create a new post",
)
def create_post(body: PostSubmit) -> Post:
    if "user_id" not in session:
        return None  # plus tard → 401 Unauthorized

    user = get_user(session["user_id"])
    if user is None:
        return None

    post = create_post_service(
        title=body.title,
        content=body.content,
        author_username=user.username,
        response_to=body.response_to,
    )

    return post.to_dict()


@api.delete(
    "/<uuid:post_id>", tags=[post_tag], responses={204: None}, summary="Delete a post"
)
def delete_post(path: PostId) -> None:
    deleted = delete_post_service(path.post_id)

    if not deleted:
        return None  # flask_openapi3 renvoie 404

    return None  # 204 No Content
