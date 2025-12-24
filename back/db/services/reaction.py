from db import db
from db.model.Reaction import Reaction


def add_reaction(post_id, username, reaction):
    r = Reaction(
        post_id=post_id,
        username=username,
        reaction=reaction,
    )
    db.session.add(r)
    db.session.commit()
    return r


def get_reactions_for_post(post_id):
    return Reaction.query.filter_by(post_id=post_id).all()


def remove_reaction(post_id, username, reaction):
    r = Reaction.query.filter_by(
        post_id=post_id,
        username=username,
        reaction=reaction,
    ).first()

    if r is None:
        return False

    db.session.delete(r)
    db.session.commit()
    return True



def clear_reactions_for_post(post_id, reaction=None):
    query = Reaction.query.filter_by(post_id=post_id)

    if reaction is not None:
        query = query.filter_by(reaction=reaction)

    count = query.delete()
    db.session.commit()
    return count
