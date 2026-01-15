from flask import session
from flask_openapi3 import APIBlueprint
from lib.make_error import make_error
from structures import PostId, PostIdWithReaction
from .tags import post_tag
from db.api.User import get_user
from db.api.Post import get_post
from db.api.Reaction import (
    add_reaction,
    remove_reaction,
    clear_reactions_for_post,
    get_reactions_summary,
    get_reaction_count,
)


api = APIBlueprint("Reactions", __name__)


@api.get("/<uuid:post_id>/reactions", tags=[post_tag])
def get_reactions_aggregate(path: PostId):
    if get_post(path.post_id) is None:
        return make_error(404, "Post not found")
    return get_reactions_summary(path.post_id)


@api.get("/<uuid:post_id>/reactions/<string:reaction>", tags=[post_tag])
def get_reaction(path: PostIdWithReaction):
    if get_post(path.post_id) is None:
        return make_error(404, "Post not found")
    count = get_reaction_count(path.post_id, path.reaction)
    return {"count": count}


@api.post("/<uuid:post_id>/reactions/<string:reaction>", tags=[post_tag])
def add_reaction_api(path: PostIdWithReaction):
    if "user_id" not in session:
        return make_error(401, "Unauthorized")
    user = get_user(session["user_id"])
    if user is None:
        return make_error(404, "User not found")

    add_reaction(str(path.post_id), user.username, path.reaction)
    return make_error(201, "Reaction added")


@api.delete("/<uuid:post_id>/reactions/<string:reaction>", tags=[post_tag])
def remove_reaction_api(path: PostIdWithReaction):
    if "user_id" not in session:
        return make_error(401, "Unauthorized")
    removed = remove_reaction(str(path.post_id), session["user_id"], path.reaction)
    if not removed:
        return make_error(404, "Reaction not found")
    return make_error(204, "Reaction removed")


@api.delete("/<uuid:post_id>/reactions/bulk", tags=[post_tag])
def bulk_remove_reaction(path: PostId):
    if "user_id" not in session:
        return make_error(401, "Unauthorized")
    clear_reactions_for_post(str(path.post_id))
    return make_error(204, "All reactions cleared")
