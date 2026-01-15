from pydantic import BaseModel


class Reaction(BaseModel):
    id: str
    post_id: str
    username: str
    reaction: str
