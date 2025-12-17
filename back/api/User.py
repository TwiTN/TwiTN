from flask_openapi3 import APIBlueprint, Tag
from structures import User, UserSignUp, UserPatch, UserLogin,UserUUID
from db import get_user, add_user, delete_user

from flask import request

api = APIBlueprint("User", __name__, url_prefix="/user")

user_tag = Tag(name="User", description="Operations related to users")

@api.get("/",
        tags=[user_tag],
        responses={200: User}
)
def get_current_user() -> User:
    raise NotImplementedError("User retrieval not implemented yet.")

@api.get(
    "/<string:uuid>",
    tags=[user_tag],
    responses={200: User},
)
def get_user_by_id(path: UserUUID):
    user = get_user(path.uuid)
    if user==None:
        return "<p>User not found</p>",200
    return user.to_dict(),200

@api.delete("/<uuid>",
        tags=[user_tag],
        responses={204: None}
)
def del_user(uuid: str) -> None:
    delete_user(uuid)

@api.post("/",
          tags=[user_tag],
          responses={201: User},
)
def create_user(
    body: UserSignUp
) -> User:
    user = add_user(body.username,body.display_name,body.email,body.password)
    if user==None:
        return {},409
    return user, 201

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