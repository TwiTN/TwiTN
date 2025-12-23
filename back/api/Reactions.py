from flask_openapi3 import APIBlueprint
from structures import PostId, PostIdWithReaction
from .tags import post_tag

api = APIBlueprint("Reactions", __name__, url_prefix="/posts")

@api.get(
    "/<uuid:post_id>/reactions",
    tags=[post_tag],
    responses={200: None},
    summary="Get an aggregate of reactions for a post",
    description="this might not be up to date because of the caching system.",
)
def get_reactions_aggregate(
    path: PostId,
):
    raise NotImplementedError("Get reactions not implemented yet.")


@api.get(
    "/<uuid:post_id>/reactions/<string:reaction>",
    tags=[post_tag],
    responses={200: None},
    summary="Get a count of a specific reaction for a post",
)
def get_reaction(
    path: PostIdWithReaction,
):
    raise NotImplementedError("Get reactions not implemented yet.")


@api.post(
    "/<uuid:post_id>/reactions/<string:reaction>",
    tags=[post_tag],
    responses={201: None},
    summary="Add a reaction to a post",
)
def add_reaction(
    path: PostIdWithReaction,
):
    raise NotImplementedError("Add reaction not implemented yet.")


@api.delete(
    "/<uuid:post_id>/reactions/<string:reaction>",
    tags=[post_tag],
    responses={201: None},
    summary="Removes a reaction to a post",
)
def remove_reaction(
    path: PostIdWithReaction,
):
    raise NotImplementedError("Remove reaction not implemented yet.")


@api.delete(
    "/<uuid:post_id>/reactions/<string:reaction>/bulk",
    tags=[post_tag],
    responses={201: None},
    summary="Removes all reactions of a specific type to a post",
)
def bulk_remove_reaction(
    path: PostIdWithReaction,
):
    raise NotImplementedError("Bulk remove reaction not implemented yet.")
