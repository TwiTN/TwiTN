from flask_openapi3 import APIBlueprint, Tag
from structures import User, UserSignUp, UserPatch, UserLogin

api = APIBlueprint("User", __name__, url_prefix="/user")

user_tag = Tag(name="User", description="Operations related to users")

@api.get("/",
        tags=[user_tag],
        responses={200: User}
)
def get_user() -> User:
    raise NotImplementedError("User retrieval not implemented yet.")

@api.get("/<uuid>",
        tags=[user_tag],
        responses={200: User}
)
def get_user_by_id(
    uuid: str,
) -> User:
    raise NotImplementedError("User retrieval by ID not implemented yet.")

@api.delete("/<uuid>",
        tags=[user_tag],
        responses={204: None}
)
def del_user(uuid: str) -> None:
    raise NotImplementedError("User deletion not implemented yet.")

@api.post("/",
          tags=[user_tag],
          responses={201: User},
)
def create_user(
    body: UserSignUp
) -> User:
    raise NotImplementedError("User creation not implemented yet.")

@api.patch("/<uuid>",
           tags=[user_tag],
           responses={200: User}
)
def update_user(uuid: str, body: UserPatch) -> User:
    raise NotImplementedError("User update not implemented yet.")

@api.post("/login",
          tags=[user_tag],
          responses={200: User})
def login_user(
    body: UserLogin
) -> User:
    raise NotImplementedError("User login not implemented yet.")