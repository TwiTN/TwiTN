from pydantic import BaseModel, Field
from bcrypt import hashpw, gensalt

class User(BaseModel):


    username: str = Field(
        description="Unique identifier for the user",
        min_length=5,
        max_length=20,
    )
    display_name: str = Field(
        description="Name displayed on the user's profile",
        max_length=50,
    )
    email: str = Field(
        description="User's email address",
        max_length=100,
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    password: str = Field(
        description="Hashed password for user authentication",
        min_length=8,
        exclude=True,
    )

    def update_password(
            self,
            new_password: str
    ):
        raise NotImplementedError("Password update not implemented yet.")
    
    def verify_password(
            self,
            password: str
    ) -> bool:
        raise NotImplementedError("Password verification not implemented yet.")