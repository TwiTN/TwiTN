from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column

from db.model.Post import Post


class PostTree(Post):
    """
    Modèle de lecture pour le résultat de get_post_tree.
    Hérite de Post et ajoute la profondeur dans l'arbre.
    """
    depth = mapped_column(Integer)
