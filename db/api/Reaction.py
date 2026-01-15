from db import db
from db.model.Reaction import Reaction
from sqlalchemy import func


def add_reaction(post_id, username, reaction):
    new_r = Reaction(post=post_id, author=username, character=reaction)
    db.session.add(new_r)

    db.session.commit()
    return True


def get_reaction_count(post_id, reaction_type):
    return Reaction.query.filter_by(post_id=post_id, reaction=reaction_type).count()


def get_reactions_summary(post_id):
    results = (
        db.session.query(Reaction.character, func.count(Reaction.character))
        .filter(Reaction.post == post_id)
        .group_by(Reaction.character)
        .all()
    )
    return {r[0]: r[1] for r in results}


def reaction_exists(post_id, username, reaction):
    existing = Reaction.query.filter_by(
        post=post_id, author=username, character=reaction
    ).first()
    return existing is not None


def remove_reaction(post_id, username, reaction):
    target = Reaction.query.filter_by(
        post=post_id, author=username, character=reaction
    ).first()
    if not target:
        return False
    db.session.delete(target)
    db.session.commit()
    return True


def clear_reactions_for_post(post_id, reaction=None):
    query = Reaction.query.filter_by(post=post_id)
    if reaction:
        query = query.filter_by(character=reaction)
    count = query.delete()
    db.session.commit()
    return count
