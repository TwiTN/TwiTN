from flask import session
from flask_openapi3 import APIBlueprint
from lib.responses import make_error, make_success
from .tags import post_tag

from db.model import Reaction, User
import structures


api = APIBlueprint("Reactions", __name__)


@api.get(
    "/<uuid:post_id>/reactions/<string:reaction>",
    tags=[post_tag],
    responses={200: structures.Count},
)
def get_reaction(path: structures.PostIdWithReaction):
    if Reaction.query.filter_by(post_id=path.post_id).first() is None:
        return make_error(404, "Post not found")
    count = Reaction.query.filter_by(
        post=path.post_id, character=path.reaction
    ).count()
    return structures.Count(count=count)


@api.post("/<uuid:post_id>/reactions/<string:reaction>", tags=[post_tag])
def add_reaction_api(path: structures.PostIdWithReaction):
    if "user_id" not in session:
        return make_error(401, "Unauthorized")
    user: User = User.query.get(session["user_id"])
    if user is None:
        return make_error(404, "User not found")

    exists = (
        Reaction.query.filter_by(
            post=path.post_id, author=user.username, character=path.reaction
        ).first()
        is not None
    )

    if exists:
        Reaction.query.session.delete(
            Reaction.query.filter_by(
                post=path.post_id, author=user.username, character=path.reaction
            ).first()
        )
        Reaction.query.session.commit()
        return make_success(200, "Reaction removed")
    else:
        new_reaction = Reaction(
            post=path.post_id, author=user.username, character=path.reaction
        )
        Reaction.query.session.add(new_reaction)
        Reaction.query.session.commit()
        return make_success(201, "Reaction added")
