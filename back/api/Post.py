from flask_openapi3 import APIBlueprint, Tag
from structures import Post, PostList, PostSubmit, GetPostQuery

api = APIBlueprint("Post", __name__, url_prefix="/posts")

post_tag = Tag(name="Post", description="Operations related to posts")

@api.get("/",
        tags=[post_tag],
        responses={200: PostList}
)
def get_posts() -> PostList:
    raise NotImplementedError("Post retrieval not implemented yet.")


@api.get("/<uuid>",
        tags=[post_tag],
        responses={200: Post}
)
def get_post_by_id(
    uuid: str,
    query: GetPostQuery
) -> Post:
    raise NotImplementedError("Post retrieval by ID not implemented yet.")

@api.post("/",
          tags=[post_tag],
          responses={201: Post},
)
def create_post(
    body: PostSubmit
) -> Post:
    raise NotImplementedError("Post creation not implemented yet.")

@api.delete("/<uuid>",
        tags=[post_tag],
        responses={204: None}
)
def del_post(uuid: str) -> None:
    raise NotImplementedError("Post deletion not implemented yet.")

