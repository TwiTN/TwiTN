from sqlalchemy import text
from db import db


def get_post_tree(root_id, max_depth):
    """
    Appelle la fonction SQL get_post_tree(root_id, max_depth)
    et retourne une liste de lignes.
    """
    sql = text("""
        SELECT *
        FROM get_post_tree(:root_id, :max_depth)
    """)

    result = db.session.execute(
        sql,
        {
            "root_id": root_id,
            "max_depth": max_depth,
        }
    )

    return result.fetchall()
def map_post_tree(rows):
    """
    Transforme le résultat SQL en dict Python exploitable.
    """
    return [
        {
            "id": str(row.id),
            "title": row.title,
            "content": row.body,
            "author": row.author,
            "response_to": str(row.reply_to) if row.reply_to else None,
            "depth": row.depth,
        }
        for row in rows
    ]
