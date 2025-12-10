from flask_openapi3 import APIBlueprint, Tag
from structures import User

api = APIBlueprint("User", __name__, url_prefix="/user")

user_tag = Tag(name="User", description="Operations related to users")

@api.get("/",
        tags=[user_tag],
        responses={200: User}
)
def get_user() -> User:
    raise NotImplementedError("User retrieval not implemented yet.")

@api.delete("/",
        tags=[user_tag],
        responses={204: None}
)
def del_user() -> None:
    raise NotImplementedError("User deletion not implemented yet.")
