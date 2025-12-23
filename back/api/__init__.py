from flask_openapi3 import APIBlueprint
from back.api.User import api as user_api
from back.api.Post import api as post_api

api = APIBlueprint("API", __name__, url_prefix="/api")
api.register_api(user_api)
api.register_api(post_api)
