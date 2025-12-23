from flask_openapi3 import APIBlueprint
from back.structures import Post, PostList, PostSubmit, DepthPaging, Paging, PostId
from .Reactions import api as reactions_api
from .tags import post_tag

api = APIBlueprint("Post", __name__, url_prefix="/posts")
api.register_api(reactions_api)


@api.get("/", tags=[post_tag], responses={200: PostList}, summary="Get a list of posts")
def get_posts(
    query: Paging,
) -> PostList:
    raise NotImplementedError("Post retrieval not implemented yet.")


@api.get(
    "/<uuid:post_id>", tags=[post_tag], responses={200: Post}, summary="Get post by ID"
)
def get_post_by_id(path: PostId, query: DepthPaging) -> Post:
    raise NotImplementedError("Post retrieval by ID not implemented yet.")


@api.post(
    "/",
    tags=[post_tag],
    responses={201: Post},
    summary="Create a new post",
)
def create_post(body: PostSubmit) -> Post:
    raise NotImplementedError("Post creation not implemented yet.")


@api.delete(
    "/<uuid:post_id>", tags=[post_tag], responses={204: None}, summary="Delete a post"
)
def delete_post(path: PostId) -> None:
    raise NotImplementedError("Post deletion not implemented yet.")
