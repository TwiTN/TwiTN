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
        default="",
    )

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "display_name": self.display_name
        }


class UserSignUp(BaseModel):
    username: str = Field(
        description="Unique identifier for the user",
        min_length=5,
        max_length=20,
        json_schema_extra={"examples":["john_doe", "jane_smith"]}
    )
    display_name: str = Field(
        description="Name displayed on the user's profile",
        max_length=50,
        json_schema_extra={"examples":["John Doe", "Jane Smith"]}
    )
    email: str = Field(
        description="User's email address",
        max_length=100,
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        json_schema_extra={"examples":["john.doe@example.com", "jane.smith@example.com"]}
    )
    password: str = Field(
        description="Password for user authentication",
        min_length=8,
        json_schema_extra={"examples":["P@ssw0rd123", "SecurePass!"]}
    )


class UserPatch(BaseModel):
    display_name: str = Field(
        description="Name displayed on the user's profile",
        max_length=50,
        json_schema_extra={"examples":["john.doe@example.com", "jane.smith@example.com"]}
    )
    email: str = Field(
        description="User's email address",
        max_length=100,
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        json_schema_extra={"examples":["john.doe@example.com", "jane.smith@example.com"]}
    )
    password: str = Field(
        description="Password for user authentication",
        min_length=8,
        json_schema_extra={"examples":["P@ssw0rd123", "SecurePass!"]}
    )


class UserLogin(BaseModel):
    username: str = Field(
        description="Unique identifier for the user",
        min_length=5,
        max_length=20,
        json_schema_extra={"examples":["john_doe", "jane_smith"]}
    )
    password: str = Field(
        description="Password for user authentication",
        min_length=8,
        json_schema_extra={"examples":["P@ssw0rd123", "SecurePass!"]}
    )


class UserId(BaseModel):
    username: str = Field(..., description="User ID (username)")
