from sqlalchemy import text
from db import db
from db.model import Post


def create_post(title, body, author, posted_at, reply_to=None) -> Post:
    post = Post(
        title=title,
        body=body,
        author=author,
        posted_at=posted_at,
        reply_to=reply_to,
    )
    db.session.add(post)
    db.session.commit()
    return post


def get_post(post_id):
    return db.session.get(Post, post_id)


def list_posts(limit=20, offset=0) -> list[Post]:
    return (
        db.session.query(Post)
        .order_by(Post.posted_at)
        .limit(limit)
        .offset(offset)
        .all()
    )


def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        return False
    db.session.delete(post)
    db.session.commit()
    return True


def get_post_tree(root_id, max_depth):
    sql = text("""
        SELECT *
        FROM get_post_tree(:root_id, :max_depth)
    """)

    return (
        db.session.execute(
            sql,
            {
                "root_id": root_id,
                "max_depth": max_depth,
            },
        )
        .scalars()
        .all()
    )
