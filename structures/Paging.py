from pydantic import BaseModel, Field


class Paging(BaseModel):
    page: int = Field(0, description="Page number", ge=1)
    size: int = Field(10, description="Number of items per page", ge=1, le=100)


class Depth(BaseModel):
    depth: int = Field(1, description="Depth level for nested resources", ge=0)
