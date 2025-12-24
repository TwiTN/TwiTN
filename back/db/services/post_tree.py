from sqlalchemy import text
from db import db


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
