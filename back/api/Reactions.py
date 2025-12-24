from flask_openapi3 import APIBlueprint
from structures import PostId, PostIdWithReaction
from .tags import post_tag
from db.services.reaction import (
    add_reaction,
    get_reactions_for_post,
    remove_reaction,
    clear_reactions_for_post,
)

api = APIBlueprint("Reactions", __name__, url_prefix="/posts")

@api.get(
    "/<uuid:post_id>/reactions",
    tags=[post_tag],
    responses={200: None},
    summary="Get an aggregate of reactions for a post",
    description="this might not be up to date because of the caching system.",
)
def get_reactions_aggregate(path: PostId):
    reactions = get_reactions_for_post(path.post_id)

    aggregate = {}
    for r in reactions:
        aggregate[r.reaction] = aggregate.get(r.reaction, 0) + 1

    return aggregate

@api.get(
    "/<uuid:post_id>/reactions/<string:reaction>",
    tags=[post_tag],
    responses={200: None},
    summary="Get a count of a specific reaction for a post",
)
def get_reaction(path: PostIdWithReaction):
    reactions = get_reactions_for_post(path.post_id)
    count = sum(1 for r in reactions if r.reaction == path.reaction)
    return {"count": count}


@api.post(
    "/<uuid:post_id>/reactions/<string:reaction>",
    tags=[post_tag],
    responses={201: None},
    summary="Add a reaction to a post",
)
def add_reaction_api(path: PostIdWithReaction):
    add_reaction(
        post_id=path.post_id,
        username="TODO",  # remplacé plus tard par la session
        reaction=path.reaction,
    )
    return None


@api.delete(
    "/<uuid:post_id>/reactions/<string:reaction>",
    tags=[post_tag],
    responses={201: None},
    summary="Removes a reaction to a post",
)
def remove_reaction_api(path: PostIdWithReaction):
    removed = remove_reaction(
        post_id=path.post_id,
        username="TODO",
    )

    if not removed:
        return None

    return None


@api.delete(
    "/<uuid:post_id>/reactions/<string:reaction>/bulk",
    tags=[post_tag],
    responses={201: None},
    summary="Removes all reactions of a specific type to a post",
)
def bulk_remove_reaction(path: PostIdWithReaction):
    clear_reactions_for_post(
        post_id=path.post_id,
        reaction=path.reaction,
    )
    return None
