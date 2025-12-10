from flask_openapi3 import APIBlueprint
from structures import Post

api = APIBlueprint("Post", __name__, url_prefix="/post")