from pydantic import BaseModel, Field


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
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    )
    password: str = Field(
        description="Hashed password for user authentication",
        min_length=8,
        exclude=True,
    )

    def update_password(self, new_password: str):
        raise NotImplementedError("Password update not implemented yet.")

    def verify_password(self, password: str) -> bool:
        raise NotImplementedError("Password verification not implemented yet.")


class UserSignUp(BaseModel):
    username: str = Field(
        description="Unique identifier for the user",
        min_length=5,
        max_length=20,
        examples=["john_doe", "jane_smith"],
    )
    display_name: str = Field(
        description="Name displayed on the user's profile",
        max_length=50,
        examples=["John Doe", "Jane Smith"],
    )
    email: str = Field(
        description="User's email address",
        max_length=100,
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        examples=["john.doe@example.com", "jane.smith@example.com"],
    )
    password: str = Field(
        description="Password for user authentication",
        min_length=8,
        examples=["P@ssw0rd123", "SecurePass!"],
    )


class UserPatch(BaseModel):
    display_name: str = Field(
        description="Name displayed on the user's profile",
        max_length=50,
        examples=["John Doe", "Jane Smith"],
    )
    email: str = Field(
        description="User's email address",
        max_length=100,
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        examples=["john.doe@example.com", "jane.smith@example.com"],
    )
    password: str = Field(
        description="Password for user authentication",
        min_length=8,
        examples=["P@ssw0rd123", "SecurePass!"],
    )


class UserLogin(BaseModel):
    username: str = Field(
        description="Unique identifier for the user",
        min_length=5,
        max_length=20,
        examples=["john_doe", "jane_smith"],
    )
    password: str = Field(
        description="Password for user authentication",
        min_length=8,
        examples=["P@ssw0rd123", "SecurePass!"]
    )

class UserId(BaseModel):
    username: str = Field(..., description="User ID (username)")

