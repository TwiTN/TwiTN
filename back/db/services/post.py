from db import db
from db.model.Post import Post


def create_post(title, content, author_username, response_to=None):
    post = Post(
        title=title,
        content=content,
        author_username=author_username,
        response_to=response_to,
    )
    db.session.add(post)
    db.session.commit()
    return post


def get_post(post_id):
    return Post.query.get(post_id)


def list_posts(limit=20, offset=0):
    return (
        Post.query
        .order_by(Post.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


def delete_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return False
    db.session.delete(post)
    db.session.commit()
    return True
