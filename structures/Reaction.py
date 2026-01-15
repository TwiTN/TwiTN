from pydantic import BaseModel, Field


class Count(BaseModel):
    count: int = Field(description="Number of reactions", ge=0)
